from math import radians, sin, cos, acos, asin, sqrt

def distance_cos(lat1, lon1, lat2, lon2, R=6371000):

    p1, p2 = radians(lat1), radians(lat2)
    dl = radians(lon1 - lon2)
    c = sin(p1) * sin(p2) + cos(p1) * cos(p2) * cos(dl)
    c = max(-1.0, min(1.0, c))     # защита от ошибок округления
    return acos(c) * R

def distance_hav(lat1, lon1, lat2, lon2, R=6371000):

    p1, p2 = radians(lat1), radians(lat2)
    dphi = p2 - p1
    dl = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * R * asin(sqrt(a))

tura   = (64.28, 100.22)
sydney = (-33.874, 151.213)
ny     = (40.71, -74.01)

print('Тура – Сидней:    %.1f км' % (distance_cos(*tura, *sydney) / 1000))
print('Тура – Нью-Йорк:  %.2f км' % (distance_cos(*tura, *ny) / 1000))