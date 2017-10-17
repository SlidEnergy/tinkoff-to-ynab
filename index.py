import csv
from datetime import datetime

sourcePath = "d:\Downloads\operations Fri Sep 01 06_44_58 MSK 2017-Fri Sep 29 09_18_05 MSK 2017.csv"
destPath = "d:\Downloads\ynab.csv"

categories = {
    #игнорируем
    "Наличные":"",
    "Переводы/иб":"",

    #для анализа
    "Другое":"",
    "Финан. услуги":"",
    "Одежда, обувь":"",
    "Разные товары":"",
    "Сервис. услуги":"",
    "Ювелирные изделия и часы":"",
    "Связь, телеком":"Фикс. месячные счета: Телефон мой и Насти",
    "Мобильные/иб":"Фикс. месячные счета: Телефон мой и Насти",

    #разбираем
    "Топливо":"Ежедневные траты: Бензин",
    "Супермаркеты":"Ежедневные траты: Продукты",
    "Фастфуд":"Ежедневные траты: Развлечение и спонтанные покупки",
    "Рестораны":"Ежедневные траты: Развлечение и спонтанные покупки",
    "Цветы":"Разовые платежи: Праздники и подарки",
    "Аптеки":"Разовые платежи: Здоровье",
    "Дом, ремонт":"Ежедневные траты: Разное"
}

descriptions = {
    "YUVOS":"Ежедневные траты: Разное",
    "Avito":"Ежедневные траты: Разное",
    "Плата за обслуживание":"Фикс. месячные счета: Разное (смс-банки)",
    "Плата за предоставление услуги SMS-банк":"Фикс. месячные счета: Разное (смс-банки)",
    "NASH DETSKIY":"Ежедневные траты: Ребенок",

    "Вознаграждение за операции покупок":"",
    "Проценты на остаток по счету":"",
}

with open(destPath, 'w', newline='',encoding="utf-8") as dest:
    writer = csv.writer(dest, delimiter=',')
    writer.writerow(["Date","Payee","Category","Memo","Outflow","Inflow"])
    
    with open(sourcePath, 'r') as source:
        reader = csv.DictReader(source, delimiter=';')
        for row in reader:

            # datetime
            date = datetime.strptime(row['Дата операции'],"%d.%m.%Y %H:%M:%S")

            # inflow & outflow
            sum = int(float(row["Сумма операции"].replace(',', '.')))
            inflow = 0
            outflow = 0
            if sum < 0:
                outflow = abs(sum)
            else: 
                inflow = sum

            # category
            category = ""
            try:
                category = categories[row["Категория"]]
            except KeyError as e:
                pass

            # description
            description = row["Описание"]

            try:
                category = descriptions[description]
            except KeyError as e:
                pass

            # validation
            # if sum == 0 or category == "":
            #     print(row)
            #     continue

            if row["Статус"] == "OK":
                writer.writerow([date.strftime("%d/%m/%Y"),"",category,description + ' (' + row["Категория"] + ')',outflow,inflow])

print ("Done")