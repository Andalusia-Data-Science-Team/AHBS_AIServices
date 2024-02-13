import requests


def translate_file(file_path: str, output_path: str, server_ip: str = None, port: int = None):
    """

    :param file_path: (str) input file path ex 'path/test.xlsx'
    :param output_path: (str) output file path ex 'path/test_english.xlsx'
    :param server_ip: (str) ex '10.24.18.37'
    :param port: (int) ex 2002
    :return: None
    """

    if server_ip is None:
        server_ip = '10.24.105.160'
    if port is None:
        port = 2002

    url = f"http://{server_ip}:{str(port)}/translate"

    files = {'excel_sheet': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"can't translate file {response.content}")
