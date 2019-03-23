
def snake_to_title(target):
    return ''.join(segment.title() for segment in target.split('_'))