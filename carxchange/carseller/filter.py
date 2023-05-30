from django.db.models import Q

def filter(cars, args):
    args = dict(args)
    if args.get('search'):
        search = args.pop('search')[0].lower()
        search_filter = Q(title__icontains=search)
        search_filter.add(Q(description__icontains=search), Q.OR)
        search_filter.add(Q(color__icontains=search), Q.OR)
        cars = cars.filter(search_filter)
    if args.get('wheel'):
        cars = cars.filter(wheel__in=args.get('wheel'))
    if args.get('transmission'):
        cars = cars.filter(transmission__in=args.get('transmission'))
    if args.get('accidents'):
        cars = cars.filter(accidents__in=args.get('accidents'))
    if args.get('fuel'):
        cars = cars.filter(fuel__in=args.get('fuel'))
    if args.get('brand'):
        cars = cars.filter(brand__in=args.get('brand'))    
    return cars