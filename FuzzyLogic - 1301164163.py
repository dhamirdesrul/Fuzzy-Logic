import numpy
import csv

#fuzzyfication dalam gaji (model trapesium)
def Penghasilan(pendapatan):
    Bawah = 0
    Tengah = 0
    Atas = 0
    if (pendapatan < 1.2): #nilai bawah untuk spesifikasi gaji/ pendapatan
        Bawah = 1
    elif (0.925 <= pendapatan <= 1.2): #nilai antara bawah dan tengah
        Bawah = (fungsiTurun(0.925, 1.2, pendapatan))
        Tengah = (fungsiNaik(1.2, 0.925, pendapatan))
    elif (1.2 <= pendapatan < 1.684): #nilai tengah untuk spesifikasi gaji/ pendapatan
        Tengah = 1
    elif (1.684 <= pendapatan <= 1.730): #nilai antara tengah dan atas
        Tengah = (fungsiTurun(1.684, 1.730, pendapatan))
        Atas = (fungsiNaik(1.730, 1.684, pendapatan))
    elif (1.730 < pendapatan): #nilai atas untuk spesifikasi gaji/pendapatan
        Atas = 1
    return Bawah, Tengah, Atas

#fuzzyfication dalam hutang
def HutangMereka(hutang):
    Kecil = 0
    Sedang = 0
    Besar = 0
    if (hutang < 28.740): #nilai batas hutang
        Kecil = 1
    elif (27.693 <= hutang <= 35.400): #nilai batas untuk antara  kecil dan sedang
        Kecil = (fungsiTurun(28.740, 35.400, hutang))
        Sedang = (fungsiNaik(35.400, 28.740, hutang))
    elif (28.740 < hutang < 68.795): #nilai batas untuk tengah
        Sedang = 1
    elif (62.427 <= hutang <= 68.795): #nilai antara untuk antara sedang dan besar
        Sedang = (fungsiTurun(68.795, 78.028, hutang))
        Besar = (fungsiNaik(78.028, 68.795, hutang))
    elif (hutang > 68.795): #nilai batas untuk besar pada hutang
        Besar = 1
    return Besar, Sedang, Kecil

#menghitung fungsi turun
def fungsiTurun(kiri, kanan, x):
    fT = (-(x - kanan)) / (kanan - kiri)
    return fT

#menghitung fungsi naik
def fungsiNaik(kiri, kanan, x):
    fN = (x - kiri) / (kanan - kiri)
    return fN

#fungsi yang digunakan untuk memasukkan nilai spesifikasi yang telah ditentukan sebelumnya untuk dapat ditentukan kelayakannya, dipertimbangkan, dan ketidaklayakannya
def gabunganyanghqq(BawahP , TengahP, AtasP, BesarH, SedangH, KecilH):
        Dipertimbangkan = [0] * 3
        Layak = [0] * 4
        Tidak_Layak = [0] * 2

        #Layak (nilai kelayakan)
        Layak[0] = (min(TengahP, SedangH))
        Layak[1] = (min(BawahP, BesarH))
        Layak[2] = (min(BawahP, SedangH))
        Layak[3] = (min(BawahP, KecilH))

        #print(Layak)

        #Dipertimbangkan (nilai pertimbangan)
        Dipertimbangkan[0]= (min(AtasP, BesarH))
        Dipertimbangkan[1] = (min(AtasP, SedangH))
        Dipertimbangkan[2] = (min(TengahP, BesarH))

        #print(Dipertimbangkan)

        #Tidak Layak (nilai ketidaklayakan)
        Tidak_Layak[0]= (min(AtasP, KecilH))
        Tidak_Layak[1] = (min(TengahP, KecilH))

        #print(Tidak_Layak)

        #inference untuk kelayakan, dipertimbangakan, dan tidak layak
        L = (max(Layak[0], Layak[1], Layak[2], Layak[3]))
        D= max(Dipertimbangkan[0], Dipertimbangkan[1], Dipertimbangkan[2])
        # print(D)
        TL= (max(Tidak_Layak[0], Tidak_Layak[1]))
        #print(L,D,TL)
        return L, D, TL

#deffuzification dhamir rajin skuy
def defuzifikasiSugeno(L, D, TL): #menentukan nilai defuzzifikasi
    #print
    Nlayak = 100
    Ndipertimbangkan = 50
    Ntidak_layak = 2
    nilaiLDTL = L + D + TL
    Total = ((L*Nlayak) + (D * Ndipertimbangkan) + (TL * Ntidak_layak))/(L+D+TL)
    return Total


#fungsi untuk memanggil elemen agar dapat dimasukkan ke dalam file csv
def getElm(orang):
    return orang[1]

if __name__ == "__main__":
    # array yang digunakan untuk memasukkan nilai csv
    dataFuzzy=[]
    # pemanggilan perulangan untukkk nilaii csv yang nantinya akan dimasukkan ke dalam array
    with open('DataTugas2.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader, None)
        for row in spamreader:
            dataFuzzy.append([int(row[0]),float(row[1]),float(row[2])])
            # print
            # ', '.join(row)
    # print(data)
    # x = []
    # y = []
    # z = []
    result = []
    # memasukkan nilai array yang sudah dimasukkan csv sebelumnya untuk mengambil nilai terhadap fungsi penghasilan dan hutang
    for i in range(len(dataFuzzy)):
        BawahP, TengahP, AtasP = Penghasilan(dataFuzzy[i][1])
        BesarH, SedangH, KecilH = HutangMereka(dataFuzzy[i][2])
        # memanggil fungsi untuk mengembalikan nilai yang berupa nilai untuk 3 kategori yakni layak, dipertimbangkan dan tidak layak
        x, y ,z = (gabunganyanghqq(BawahP , TengahP, AtasP, BesarH, SedangH, KecilH))
        tot = defuzifikasiSugeno(x,y,z)
        # print('No: ', i+1)
        # print('Layak: ', x)
        # print('Dipertimbangkan : ', y)
        # print('Tidak Layak: ', z)
        # print('Sugeno: ', tot)
        result.append([i+1, tot])
    print('Kesimpulan: ')
    print(result) #menampilkan hasil
    result.sort(key=getElm, reverse=True)
    print('Pengurutan Kelayakan: ')
    print(result)
    resultFix = []
    #memasukkan 20 orang yang layak dapat bantuan ke dalam array
    for i in range(20):
        resultFix.append(result[i][0])
    print('20 Orang yang diterima: ')
    print(resultFix)
    #memasukkan nilai ke dalam csv
    numpy.savetxt('TebakanTugas2.csv', resultFix, delimiter=',', fmt='%s')