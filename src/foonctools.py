def modified_(kline:list):
    """
    Перевод значений входящего клайна из строкового типа данных в числовой
    """
    return {
        'open': float(kline[1]),
        'high': float(kline[2]),
        'low': float(kline[3]),
        'close': float(kline[4]),
        'volume': float(kline[5])
    }
