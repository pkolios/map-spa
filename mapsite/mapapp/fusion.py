import hashlib
import json

import httplib2
from apiclient import discovery
from django.core.serializers.json import DjangoJSONEncoder
from oauth2client import client


class FusionAPI():
    def __init__(self, request, settings):
        self.authenticate(request)
        self.table_id = settings.GOOGLE_FUSION_TABLE_ID
        http_auth = self.credentials.authorize(httplib2.Http())
        self.fusiontables = discovery.build(
            'fusiontables', 'v2', http=http_auth)

    def authenticate(self, request):
        """Try to get credentials from the session or raise LoginRequired."""
        if 'credentials' not in request.session:
            raise LoginRequired()
        self.credentials = client.OAuth2Credentials.from_json(
            request.session['credentials'])
        if self.credentials.access_token_expired:
            raise LoginRequired()

    def _calculate_hash(self, entry):
        """Calculate a checksum hash for the entry."""
        entry.pop('id', None)
        return hashlib.sha224(json.dumps(
            entry, cls=DjangoJSONEncoder).encode('utf-8')).hexdigest()

    def get_entry(self, entry):
        """Look up entry by hash and return matched row(s)."""
        hash_key = self._calculate_hash(entry)
        sql = "SELECT * FROM {t_id} WHERE hash = '{hash_key}'".format(
            t_id=self.table_id, hash_key=hash_key)
        resp = self.fusiontables.query().sql(sql=sql).execute()
        return resp.get('rows')

    def add_entry(self, entry):
        """Add a new entry if it doesn't already exist."""
        if self.get_entry(entry):
            return entry

        keys, values = [], []
        for i in entry:
            keys.append("'{}'".format(i))
            if not isinstance(entry[i], str):
                values.append("'{}'".format(str(entry[i])))
            else:
                values.append("'{}'".format(entry[i]))

        keys.append("'hash'")
        values.append("'{}'".format(self._calculate_hash(entry)))
        sql = 'INSERT INTO {t_id} ({keys}) VALUES ({values})'.format(
            t_id=self.table_id, keys=','.join(keys), values=','.join(values))
        self.fusiontables.query().sql(sql=sql).execute()

    def purge(self):
        """Delete all rows of the table."""
        sql = "DELETE FROM {t_id}".format(t_id=self.table_id)
        self.fusiontables.query().sql(sql=sql).execute()


class LoginRequired(Exception):
    """Raise when Fusion API is not authenticated."""
