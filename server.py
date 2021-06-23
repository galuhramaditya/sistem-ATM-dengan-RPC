from xmlrpc.server import SimpleXMLRPCServer
import datetime

server_ip = "0.0.0.0"
server_port = 8008

with SimpleXMLRPCServer((server_ip, server_port), allow_none=True) as server:
    server.register_introspection_functions()

    class ATMServer:
        def __init__(self):
            self.nasabah = [
                {
                    "nama": "ABC DEF",
                    "nomor_kartu": "1234123412341234",
                    "nomor_rekening": "123123123",
                    "pin": "123456",
                    "saldo": 1000000,
                    "history": [
                        {"tanggal": "01/06/2021", "uraian": "transfer dari ZER LPO", "nominal": 20000},
                        {"tanggal": "04/06/2021", "uraian": "tarik tunai", "nominal": -150000},
                        {"tanggal": "06/06/2021", "uraian": "top up echannel kartu", "nominal": -50000},
                        {"tanggal": "10/06/2021", "uraian": "transfer ke FED CBA", "nominal": -120000},
                        {"tanggal": "10/06/2021", "uraian": "top up echannel", "nominal": -130000},
                        {"tanggal": "17/06/2021", "uraian": "top up gopay", "nominal": -100000},
                        {"tanggal": "20/06/2021", "uraian": "transfer dari LL PAK", "nominal": 56000},
                        {"tanggal": "21/06/2021", "uraian": "top up echannel", "nominal": -250000},
                    ]
                },
                {
                    "nama": "FED CBA",
                    "nomor_kartu": "4321432143214321",
                    "nomor_rekening": "321321321",
                    "pin": "654321",
                    "saldo": 2000000,
                    "history": [
                        {"tanggal": "01/06/2021", "uraian": "biaya administrasi", "nominal": -5000},
                        {"tanggal": "09/06/2021", "uraian": "top up echannel", "nominal": -120000},
                        {"tanggal": "10/06/2021", "uraian": "transfer dari ABC DEF", "nominal": 130000},
                        {"tanggal": "11/06/2021", "uraian": "top up echannel", "nominal": -100000},
                        {"tanggal": "17/06/2021", "uraian": "transfer ke POPLO", "nominal": -20000},
                        {"tanggal": "20/06/2021", "uraian": "top up shopeepay", "nominal": -350000},
                    ]
                },
            ]

        def tambah_history(self, idx_nasabah, nominal, uraian):
            self.nasabah[idx_nasabah]["history"].append({
                "tanggal": datetime.date.today().strftime("%d/%m/%Y"), "uraian": uraian,
                "nominal": nominal
            })

        def check_pin(self, idx_nasabah, pin):
            if pin == self.nasabah[idx_nasabah]["pin"]:
                return True
            return False

        def get_saldo(self, idx_nasabah):
            return self.nasabah[idx_nasabah]["saldo"]

        def get_mutasi(self, idx_nasabah, n):
            return self.nasabah[idx_nasabah]["history"][:-n:-1]

        def get_history(self, idx_nasabah, n):
            history = self.nasabah[idx_nasabah]["history"][::-1]
            result = []
            for data in history:
                tgl_sekarang = datetime.date.today()
                tgl_history = datetime.datetime.strptime(data["tanggal"], "%d/%m/%Y").date()
                selisih = tgl_sekarang - tgl_history

                if selisih > n:
                    break

                result.append(data)
            return result[::-1]

        def get_nasabah_by_nomor_kartu(self, nomor_kartu):
            for idx_nasabah, nasabah in enumerate(self.nasabah):
                if nomor_kartu == nasabah["nomor_kartu"]:
                    return idx_nasabah
            return None

        def get_nasabah_by_nomor_rekening(self, nomor_rekening):
            for idx_nasabah, nasabah in enumerate(self.nasabah):
                if nomor_rekening == nasabah["nomor_rekening"]:
                    return idx_nasabah, nasabah["nama"]
            return None, None

        def tarik_tunai(self, idx_nasabah, nominal):
            if self.get_saldo(idx_nasabah) >= nominal:
                self.nasabah[idx_nasabah]["saldo"] -= nominal
                self.tambah_history(idx_nasabah, -nominal, "tarik tunai")
                return True
            return False

        def transfer(self, idx_pengirim, idx_penerima, nominal):
            if self.get_saldo(idx_pengirim) >= nominal:
                self.nasabah[idx_pengirim]["saldo"] -= nominal
                self.nasabah[idx_penerima]["saldo"] += nominal

                self.tambah_history(idx_pengirim, -nominal, f"transfer ke {self.nasabah[idx_penerima]['nama']}")
                self.tambah_history(idx_penerima, nominal, f"transfer dari {self.nasabah[idx_pengirim]['nama']}")
                return True
            return False

    server.register_instance(ATMServer())
    server.serve_forever()
