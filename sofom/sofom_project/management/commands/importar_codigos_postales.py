import csv
import os
from django.core.management.base import BaseCommand
from sofom_project.models import CodigoPostal

class Command(BaseCommand):
    help = 'Importar datos desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Si no es una ruta absoluta, conviértelo en una
        if not os.path.isabs(csv_file):
            csv_file = os.path.join(os.getcwd(), csv_file)

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Omitir encabezados si están presentes
                for row in reader:
                    if len(row) >= 4:  # Asegúrate de que haya suficientes columnas
                        codigo_postal = row[0]  # Primera columna
                        estado = row[1]
                        municipio = row[2]
                        colonia = row[3]

                        CodigoPostal.objects.create(
                            codigo_postal=codigo_postal,
                            estado=estado,
                            municipio=municipio,
                            colonia=colonia
                        )
            self.stdout.write(self.style.SUCCESS('Datos importados con éxito'))
        except UnicodeDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error al leer el archivo: {e}'))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'Archivo no encontrado: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error inesperado: {e}'))
