from datetime import datetime

def get_current_date_formatted():
    now = datetime.utcnow()
    return now.strftime('%a, %d %b %Y %H:%M:%S GMT')

if __name__ == '__main__':
    # Пример использования:
    print(get_current_date_formatted())
