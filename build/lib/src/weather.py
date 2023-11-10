class weather:
    def isCold(temperature):
        if temperature <= 15:
            return True
        else:
            return False

    def isRainy(precipitation):
        if precipitation > 0:
            return True
        else:
            return False
