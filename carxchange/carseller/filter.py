from django.db.models import Q

def filter(cars, args):
    print(len(cars))
    args = dict(args)
    if args.get('search'):
        search = args.pop('search')[0].lower()
        search_filter = Q(title__icontains=search)
        search_filter.add(Q(description__icontains=search), Q.OR)
        search_filter.add(Q(color__icontains=search), Q.OR)
        cars = cars.filter(search_filter)
    print(len(cars))
    if args.get('wheel'):
        cars = cars.filter(wheel__in=args.get('wheel'))
    print(len(cars))
    if args.get('transmission'):
        cars = cars.filter(transmisson__in=args.get('transmission'))
    print(len(cars))
    if args.get('accidents'):
        cars = cars.filter(accidents__in=args.get('accidents'))
    print(len(cars))
    if args.get('fuel'):
        cars = cars.filter(fuel__in=args.get('fuel'))
    print(len(cars))
    if args.get('brand'):
        cars = cars.filter(brand__in=args.get('brand'))   
    print(len(cars)) 
    return cars