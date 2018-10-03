import csv
from cataloger.models import BureauCode, Division, Office

def bureau_import(csvfile):
    decoded_file = csvfile.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        if len(row['division']) == 0:
            # bureau code
            bureau = BureauCode()
            bureau.code = row['fund_center']
            bureau.description = row['description']
            bureau.save()
    csvfile.seek(0)
    decoded_file = csvfile.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        if row['division'] == row['fund_center']:
            # division
            division = Division()
            division.division = row['fund_center']
            division.bureau = BureauCode.objects.get(code=row['business_area'])
            division.description = row['description']
            division.save()
    csvfile.seek(0)
    decoded_file = csvfile.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        if len(row['fund_center']) == 10:
            # office
            office = Office()
            office.office = row['fund_center']
            office.bureau = BureauCode.objects.get(code=row['business_area'])
            office.division = Division.objects.get(division=row['division'])
            office.description = row['description']
            office.save()

