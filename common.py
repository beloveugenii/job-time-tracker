# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

def str_to_float(str=0):
# Пробуем преобразовать переданную строку в число с точкой
# Возращает его или 0.0
    try:
        str = float(str)
    except:
        str = 0.0

    return str

def isfloat(what):
# Проверяет, что переданное число является числом с точкой
# Возвращает логическое значение
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def is_valid(value, type_str, char_list = None):

    v_types = ( 'is_number', 'is_num', 'is_float', 'is_fl',
        'is_negative', 'is_neg', 'in_lst', 'in_ls', 'len_g', )

    if type_str not in v_types:
        raise ValueError(f'"{type_str}" is not implemented yet')

    value = str(value).strip()

    return (
        type_str.startswith('is_num') and value.isnumeric() or
        type_str.startswith('is_neg') and value.startswith('-') or
        type_str.startswith('is_fl') and isfloat(value) or
        type_str.startswith('in_ls') and value in char_list# or
        #  type_str.startswith('len_g') and len(value) >
    )





