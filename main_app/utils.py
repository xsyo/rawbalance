def img_upload_function(instance, filename):
    '''Возвращяет название загруженого файла'''

    file_type = filename.split('.')[-1]
    new_filename = f'{instance.title}.{file_type}'
    return new_filename