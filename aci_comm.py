import requests
import urllib3


class AciComm:

    def __init__(self, api_path, username, password):

        self.api_path = f"https://{api_path}"
        self._auth_body = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}
        self._auth_header = None

        urllib3.disable_warnings()

    @property
    def auth_header(self):
        if self._auth_header:
            return True
        return False

    def do_login(self):
        auth_resp = requests.post(f"{self.api_path}/aaaLogin.json", json=self._auth_body, verify=False)

        try:
            auth_resp.raise_for_status()
        except requests.HTTPError as e:
            print(str(e))
            return None

        token = auth_resp.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
        self._auth_header = {"Cookie": f"APIC-Cookie={token}"}

    def get_endpoint_groups(self):

        epg_resp = requests.get(f"{self.api_path}/class/fvAEPg.json", headers=self._auth_header, verify=False)

        try:
            epg_resp.raise_for_status()
        except requests.HTTPError as e:
            print(str(e))
            return None

        return epg_resp.json()


def main():

    aci = AciComm(api_path='sandboxapicdc.cisco.com/api', username='admin', password='!v3G@!4@Y')
    if not aci.auth_header:
        aci.do_login()
    epgs = aci.get_endpoint_groups()

    if epgs:
        print(f"EPGs found: {epgs['totalCount']}")
        for epg in epgs["imdata"]:
            print(f"  Name: {epg['fvAEPg']['attributes']['dn']}")


if __name__ == '__main__':
    main()
