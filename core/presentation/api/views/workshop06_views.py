# -*- coding: utf-8 -*-
import os
from lxml import etree
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Directory containing the XML files
directory = 'XML workshop 06'

def get_path_and_filename(directory):
    """
    Generates the full path and filename for each file in the specified directory.
    """
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        yield path, filename


def get_URI_and_tag(version):
    if not version == '3.3':
        URI_AND_TAG = {
            'EMISOR': '{http://www.sat.gob.mx/cfd/4}Emisor',
            'RECEPTOR': '{http://www.sat.gob.mx/cfd/4}Receptor',
            'COMPLEMENTO': '{http://www.sat.gob.mx/cfd/4}Complemento',
            'CONCEPTO': '{http://www.sat.gob.mx/cfd/4}Concepto',
            'RETENCION': '{http://www.sat.gob.mx/cfd/4}Retencion',
            'TRASLADO': '{http://www.sat.gob.mx/cfd/4}Traslado',
            'TIMBRE': '{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital',
        }
        return URI_AND_TAG
    
    URI_AND_TAG = {
        'EMISOR': '{http://www.sat.gob.mx/cfd/3}Emisor',
        'RECEPTOR': '{http://www.sat.gob.mx/cfd/3}Receptor',
        'COMPLEMENTO': '{http://www.sat.gob.mx/cfd/3}Complemento',
        'CONCEPTO': '{http://www.sat.gob.mx/cfd/3}Concepto',
        'RETENCION': '{http://www.sat.gob.mx/cfd/3}Retencion',
        'TRASLADO': '{http://www.sat.gob.mx/cfd/3}Traslado',
        'TIMBRE': '{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital',
    }
    return URI_AND_TAG


def parse_xml_file(path):
    """
    Parses the XML file and returns the root, version elements.
    """
    if not os.path.exists(path):
        error_msg = (f"Archivo no encontrado en la ruta: {path}")
        raise FileNotFoundError(error_msg)

    try:
        tree = etree.parse(path)
        root = tree.getroot()
        version = root.get('Version')
        return root, version
    except etree.XMLSyntaxError as e:
        error_msg = (f'Error de sintaxis XML del archivo de la ruta: {path}'
                    f'Linea {e.position[0]}, Columna {e.position[1]}-msg')
        raise etree.XMLSyntaxError(error_msg) from e
    except Exception as e:
        error_msg = (f'Error ocurrido{e}:')
        raise Exception(error_msg) from e


def write_a_json_file(data, name_file):
    with open(name_file, 'w', encoding='utf-8') as json_file:
        try:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        except TypeError as e:
            raise


def calculate_the_total_of_traslado(path):
    total_of_traslado = {
        '001': 0.0,
        '002': 0.0,
    }
    root, version = parse_xml_file(path)
    traslados   = root.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=root.nsmap)

    if traslados:
        for traslado in traslados:
            impuesto = traslado.get('Impuesto')
            monto = float(traslado.get('Importe'))

            if impuesto == '001': # ISR
                total_of_traslado['001'] += monto

            elif impuesto == '002': # IVA
                total_of_traslado['002'] += monto
    return total_of_traslado


def calculate_the_total_of_retencion(path):
    total_of_retencion = {
            '001': 0.0,
            '002': 0.0,
            }
    root, version = parse_xml_file(path)
    retenciones = root.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=root.nsmap)
    
    if retenciones:
        for retencion in retenciones:
            impuesto = retencion.get('Impuesto')
            monto = float(retencion.get('Importe'))

            if impuesto == '001': # ISR
                total_of_retencion['001'] += monto
                                    
            elif impuesto == '002': # IVA
                total_of_retencion['002'] += monto

    return total_of_retencion


def calculate_the_total_of_base_type_of_traslado(path):
    root, version = parse_xml_file(path)
    total_by_base_type_of_traslado = {
            'IVA general 16%': 0.0,
            'IVA Exento 00%': 0.0,
        }

    traslados   = root.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=root.nsmap)

    if traslados:
        for traslado in traslados:
            monto = float(traslado.get('Importe'))
            tasa_o_cuota = traslado.get('TasaOCuota')

            if tasa_o_cuota == '0.160000':
                total_by_base_type_of_traslado['IVA general 16%'] =+ monto
            elif tasa_o_cuota == '0.000000':
                total_by_base_type_of_traslado['IVA Exento 00%'] =+ monto

    return total_by_base_type_of_traslado


def calculate_the_total_by_base_type_of_retencion(path):
    root, version = parse_xml_file(path)
    total_by_base_type_of_retencion = {
            'IVA general 16%': 0.0,
            'IVA Exento 00%': 0.0,
        }
    retenciones = root.xpath('//cfdi:Comprobante/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=root.nsmap)
    if retenciones:
        for retencion in retenciones:
            monto = float(retencion.get('Importe'))
            tasa_o_cuota = retencion.get('TasaOCuota')

            if tasa_o_cuota == '0.160000':
                total_by_base_type_of_retencion['IVA general 16%'] =+ monto
            elif tasa_o_cuota == '0.000000':
                total_by_base_type_of_retencion['IVA Exento 00%'] =+ monto  

    return total_by_base_type_of_retencion


@api_view(['POST'])
def activity_one(request):
    print('Actividad 1: Lectura de archivos XML')
    print('-------------------------------------')
    i = 0
    for path, filename in get_path_and_filename(directory):
        try:
            # Parse the XML file
            root, version = parse_xml_file(path)
            tipo = root.get('TipoDeComprobante')
            
            # Get the URI and tag based on the version
            URI_AND_TAG = get_URI_and_tag(version)
            
            # Find the Emisor and Receptor elements
            RFC_Emisor = root.find(f'.//{URI_AND_TAG['EMISOR']}').get('Rfc')
            RFC_Receptor = root.find(f'.//{URI_AND_TAG['RECEPTOR']}').get('Rfc')
            i += 1
            
            # Print the information
            print(f'\nArchivo: {i}')
            print(f'Nombre archivo: {filename}')
            print(f'tipo: {tipo}, versión: {version}')
            print(f'RFC del Emisor: {RFC_Emisor}')
            print(f'RFC del Receptor: {RFC_Receptor}')
        
        except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
            print(f'Error al procesar el archivo {filename}: {str(e)}')
    
    return Response({'message': 'revise su consola'})
            
@api_view(['POST'])
def activity_two(request):
    print('Actividad 2')
    print('-------------------------------------')
    i= 0
    for path, filename in get_path_and_filename(directory):
        try:
            # Parse the XML file
            root, version = parse_xml_file(path)
            namespaces = root.nsmap
            espacio_de_nombre = {}
            i += 1
            
            # Print the file information
            print(f'\nArchivo: {i}')
            print(f'Nombre archivo: {filename}')
            print(f'Versión: {version}')

            for prefix, uri in namespaces.items():
                espacio_de_nombre[prefix] = uri
                # print(f"namespace: {prefix}={uri}")

            URI_AND_TAG  = get_URI_and_tag(version)
            complement = root.find(f'.//{URI_AND_TAG['COMPLEMENTO']}')
            
            # Print the information
            print(f'Todos los namespaces: {espacio_de_nombre}')        
            if complement:
                print(f'Complemento encontrado: {URI_AND_TAG['COMPLEMENTO']}')
                for child in complement:
                    print(f'Etiqueta: {child.tag}, Atributos: {child.attrib}')
            else:
                print('No se encontró el complemento.')
            print(f'\n')

        except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
            print(f'Error al procesar el archivo {filename}: {str(e)}')
    
    return Response({'message': 'revise su consola'})
            
@api_view(['POST'])
def activity_three(request):
    print('Actividad 3')
    print('-------------------------------------')
    i= 0
    data = {}

    for path, filename in get_path_and_filename(directory):
        i += 1
        try:
            # Parse the XML file
            root, version = parse_xml_file(path)
            URI_AND_TAG = get_URI_and_tag(version)
            conceptos = root.findall(f'.//{URI_AND_TAG['CONCEPTO']}')
            # Ccapture the data
            if conceptos:
                j = 0
                data[filename] = {
                        'Ruta': path,
                        'Version': version, 
                        'Conceptos': {}
                }
                for concepto in conceptos:
                    j += 1
                    data[filename]['Conceptos'][j] = {
                        'ClaveProdServ': concepto.get('ClaveProdServ'),
                        'Descripcion': concepto.get('Descripcion'),
                        'Importe': concepto.get('Importe'),
                        'ValorUnitario': concepto.get('ValorUnitario')
                    }

        except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
            print(f'Error al procesar el archivo {filename}: {str(e)}')
            data[filename] = {
                'Ruta': path,
                'Error': f'Error al procesar el archivo: {str(e)}'
            }
        
    # Save the data to a JSON file
    try:
        write_a_json_file(data=data, name_file='activity3.json')
    except TypeError as e:
        print(f'Error al serializar el objeto a JSON: {str(e)}')

    return Response({'message': 'se ha creado el archivo activity3.json, revise su directorio'})

@api_view(['POST'])
def activity_four(request):
    print('Actividad 4')
    print('-------------------------------------')

    # Define path
    path= 'XML workshop 06\\4405970a-857a-430d-8174-d42b538af065.xml'
    
    try:
        # calculate values
        total_of_traslado = calculate_the_total_of_traslado(path)
        total_by_base_type_of_traslado = calculate_the_total_of_base_type_of_traslado(path)
        total_of_retencion = calculate_the_total_of_retencion(path)
        total_by_base_type_of_retencion = calculate_the_total_by_base_type_of_retencion(path)

        # print information of retencion
        print('Total de retenciones:')
        print('\tISR:', total_of_retencion['001'])
        print('\tIVA:', total_of_retencion['002'])
        if  total_by_base_type_of_retencion['IVA general 16%'] > 0.0:
            print('\tIVA general 16%:', total_by_base_type_of_retencion['IVA general 16%'])
        if total_by_base_type_of_retencion['IVA Exento 00%'] > 0.0:
            print('\tIVA Exento 00%:', total_by_base_type_of_retencion['IVA Exento 00%'])

        # print information of traslado
        print('Total de traslados:')
        print('\tISR:', total_of_traslado['001'])
        print('\tIVA:', total_of_traslado['002'])
        if  total_by_base_type_of_traslado['IVA general 16%'] > 0.0:
            print('\tIVA general 16%:', total_by_base_type_of_traslado['IVA general 16%'])
        if total_by_base_type_of_traslado['IVA Exento 00%'] > 0.0:
            print('\tIVA Exento 00%:', total_by_base_type_of_traslado['IVA Exento 00%'])

    except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
        print(f'Error al procesar el archivo {path}: {str(e)}')

    return Response({'message': 'revise su consola'})

@api_view(['POST'])
def activity_five(request):
    print('Actividad 5')
    print('-------------------------------------')
    i= 0
    data = {}
    for path, filename in get_path_and_filename(directory):
        i += 1
        try:
            # Parse the XML file
            root, version = parse_xml_file(path)
            URI_AND_TAG = get_URI_and_tag(version)
            timbre_fiscal_digital = root.findall(f'.//{URI_AND_TAG['TIMBRE']}')

            # capture the data
            if timbre_fiscal_digital:
                data[filename] = {
                    'Ruta': path,
                    'TimbreFiscalDigital': {}
                }
                for timbre in timbre_fiscal_digital:
                    data[filename]['TimbreFiscalDigital'] = {
                        'UUID': timbre.get('UUID'),
                    }
            else:
                data[filename] = {
                    'Ruta': path,
                    'Version': version, 
                    'TimbreFiscalDigital': 'No se encontró el Timbre Fiscal Digital'
                }
        except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
            print(f'Error al procesar el archivo {path}: {str(e)}')
    
    # Save the data to a JSON file
    try:
        write_a_json_file(data=data, name_file='activity5.json')
    except TypeError as e:
        print(f'Error al serializar el objeto a JSON: {str(e)}')
    
    return Response({'message': 'se ha creado el archivo activity5.json, revise su directorio'})

@api_view(['POST'])
def activity_six(request):
    print('Actividad 6')
    print('-------------------------------------')
    i= 0
    cfdi = {}

    for path, filename in get_path_and_filename(directory):
        i += 1
        try:
            # Parse the XML file
            root, version = parse_xml_file(path)
            URI_AND_TAG = get_URI_and_tag(version)
            conceptos = root.findall(f'.//{URI_AND_TAG['CONCEPTO']}')

            if conceptos:
                #capture the data
                j = 0
                cfdi[filename] = {
                        'Ruta': path,
                        'Version': version, 
                        'Conceptos': {}
                }
                for concepto in conceptos:
                    j += 1
                    cfdi[filename]['Conceptos'][j] = {
                        'ClaveProdServ': concepto.get('ClaveProdServ'),
                        'Descripcion': concepto.get('Descripcion'),
                        'Importe': concepto.get('Importe'),
                        'ValorUnitario': concepto.get('ValorUnitario')
                    }
                    retenciones = concepto.findall(f'.//{URI_AND_TAG['RETENCION']}')
                    traslados = concepto.findall(f'.//{URI_AND_TAG['TRASLADO']}')

                    if retenciones:
                        # Initialize Retenciones if they exist
                        x = 0
                        cfdi[filename]['Conceptos'][j]['Retenciones'] = {}

                        # Iterate through Traslados and add them to the dictionary
                        for retencion in retenciones:
                            x += 1
                            impuesto = retencion.get('Impuesto')
                            importe = retencion.get('Importe')
                            tasa_o_cuota = retencion.get('TasaOCuota')
                            cfdi[filename]['Conceptos'][j]['Retenciones'][x] = {
                                'impuesto': impuesto,
                                'Importe': importe,
                                'TasaOCuota': tasa_o_cuota
                            }

                    if traslados:
                        # Initialize Traslados if they exist
                        x = 0
                        cfdi[filename]['Conceptos'][j]['Traslados'] = {}
                        
                        # Iterate through Traslados and add them to the dictionary
                        for traslado in traslados:
                            x += 1
                            impuesto = traslado.get('Impuesto')
                            importe = traslado.get('Importe')
                            tasa_o_cuota = traslado.get('TasaOCuota')
                            cfdi[filename]['Conceptos'][j]['Traslados'][x] = {
                                'Impuesto': impuesto,
                                'Importe': importe,
                                'TasaOCuota': tasa_o_cuota
                            }
            else:
                cfdi[filename] = {
                    'Ruta': path,
                    'Version': version, 
                    'Conceptos': 'No se encontraron conceptos'
                }
        
        except (FileNotFoundError, etree.XMLSyntaxError, Exception ) as e:
            print(f'Error al procesar el archivo {path}: {str(e)}')
        
    try:
        write_a_json_file(data=cfdi, name_file='cfdis.json')
    except TypeError as e:
        print(f'Error al serializar el objeto a JSON: {str(e)}')

    return Response({'message': 'se ha creado el archivo cfdis.json, revise su directorio'})
