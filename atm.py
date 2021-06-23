import xmlrpc.client
import sys


server_ip = "127.0.0.1"
server_port = 8008

server = xmlrpc.client.Server(f'http://{server_ip}:{server_port}')


class ATM:
    def __init__(self, server, nominal_pecahan):
        self.server = server
        self.nominal_pecahan = nominal_pecahan

    def validasi_nomor_kartu(self):
        for i in range(4):
            if i == 3:
                sys.exit(0)

            nomor_kartu = input("nomor kartu\t: ")
            self.idx_nasabah = self.server.get_nasabah_by_nomor_kartu(
                nomor_kartu)

            if self.idx_nasabah is not None:
                break

            print("nomor kartu tidak terdaftar")

    def validasi_pin(self):
        for i in range(4):
            if i == 3:
                sys.exit(0)

            pin = input("pin\t\t: ")
            self.valid = self.server.check_pin(self.idx_nasabah, pin)

            if self.valid:
                break

            print("pin salah")

    def cek_saldo(self):
        saldo = self.server.get_saldo(self.idx_nasabah)
        print(f"saldo anda : Rp.{saldo}")

    def tarik_tunai(self, nominal):
        if nominal % self.nominal_pecahan != 0:
            return False

        success = self.server.tarik_tunai(self.idx_nasabah, nominal)
        if success:
            self.print_line_break()
            print("silahkan ambil uang anda")
            self.print_border()
            self.cek_saldo()
        else:
            print("saldo anda tidak mencukupi")

        self.print_konfirmasi_lanjut()

        return True

    def transfer(self):
        self.print_line_break()
        while True:
            nomor_rekening = input("masukan nomor rekening\t\t: ")
            idx_penerima, nama_penerima = self.server.get_nasabah_by_nomor_rekening(
                nomor_rekening)

            if idx_penerima is None:
                print("nomor rekening tidak terdaftar")
            else:
                print(f"atas nama\t\t\t: {nama_penerima}")
                self.print_border()
                if input("apakah peneriman sudah benar? (y/n) : ") == "y":
                    break

        self.print_border()
        nominal = input("silahkan masukan nominal\t: ")

        success = self.server.transfer(self.idx_nasabah, idx_penerima, int(nominal))
        if success:
            self.print_line_break()
            print("transaksi anda berhasil")
            self.print_border()
            self.cek_saldo()
        else:
            print("saldo anda tidak mencukupi")

        self.print_konfirmasi_lanjut()

    def mutasi(self, n=5):
        self.print_line_break()
        print(f"{n} transaksi terakhir")
        for history in self.server.get_mutasi(self.idx_nasabah, n):
            print(f"{history['tanggal']}\t{history['nominal']}\t{history['uraian']}")
        self.print_konfirmasi_lanjut()

    def history(self, n=30):
        self.print_line_break()
        print(f"transaksi {n} hari terakhir")
        for history in self.server.get_mutasi(self.idx_nasabah, n):
            print(f"{history['tanggal']}\t{history['nominal']}\t{history['uraian']}")
        self.print_konfirmasi_lanjut()

    def print_konfirmasi_lanjut(self):
        self.print_border()

        if input("apakah anda ingin keluar? (y/n) : ") == "y":
            sys.exit(0)

    def print_line_break(self, n=20):
        print("\n"*n)

    def print_border(self, n=20):
        print("="*n)

    def UI(self):
        print("SELAMAT DATANG DI ATM")
        self.print_line_break(5)
        self.print_border()
        print("silahkan masukan nomor kartu anda")
        self.validasi_nomor_kartu()
        self.print_border()
        print("silahkan masukan pin anda")
        self.validasi_pin()

        while True:
            self.print_line_break()
            print(f"Silahkan Pilih Jumlah Penarikan (nominal pecahan Rp.{self.nominal_pecahan})")
            print(f"1. {self.nominal_pecahan * 1}")
            print(f"2. {self.nominal_pecahan * 2}")
            print(f"3. {self.nominal_pecahan * 5}")
            print(f"4. {self.nominal_pecahan * 10}")
            print(f"5. penarikan jumlah lain")
            print(f"6. cek saldo")
            print(f"7. transfer")
            print(f"8. mutasi rekening")
            print(f"9. history transaksi")
            print(f"10. keluar")
            pilihan = input("pilih menu : ")

            if pilihan == "10":
                sys.exit(0)
            elif pilihan == "1":
                self.tarik_tunai(self.nominal_pecahan * 1)
            elif pilihan == "2":
                self.tarik_tunai(self.nominal_pecahan * 2)
            elif pilihan == "3":
                self.tarik_tunai(self.nominal_pecahan * 5)
            elif pilihan == "4":
                self.tarik_tunai(self.nominal_pecahan * 10)
            elif pilihan == "5":
                while True:
                    self.print_line_break()
                    nominal = input("masukan nominal yang ingin ditarik : ")
                    success = self.tarik_tunai(int(nominal))
                    if success:
                        break
                    else:
                        self.print_border()
                        print("nominal tidak sesuai dengan pecahan di ATM")
            elif pilihan == "6":
                self.print_line_break()
                self.cek_saldo()
                self.print_konfirmasi_lanjut()
            elif pilihan == "7":
                self.transfer()
            elif pilihan == "8":
                self.mutasi()
            elif pilihan == "9":
                self.history()

atm = ATM(server,  50000)
atm.UI()