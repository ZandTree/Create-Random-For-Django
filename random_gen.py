import random
import string


# using only uppercase + digits

def make_random_id(chars=(string.ascii_uppercase +string.digits),size=4):
    """
    return string made of random (ascii-chars,digits)of length = size
    """
    output = [random.choice(chars) for _ in range(size)]
    return "".join(output)

print(make_random_id())
print(make_random_id())
print(make_random_id())

# using upper and lower case ascii _ digits

def rand_string(n):
    """
    return a string from ascii chars with random letters and numbers
    """
    mix = string.ascii_letters + string.digits
    final_string = [random.choice(mix) for item in range(n)]
    return "".join(final_string)

# info about dif instance.__class__(vs instance.__class__.__name__
"""
>>> s = A()
>>> one = s.__class__         # type(class)
>>> one
<class '__main__.A'> 
>>> two = s.__class__.__name__
>>> two
'A'                           #type(string)
>>>
"""



def create_profile_uid(instance):
    """
    create unique id for instance based on random letters and digits
    which have attr = uid
    """
    klass = instance.__class__
    start_unid = rand_string(4)
    if klass.objects.filter(unid=start_unid).exists():
        instance.unid = rand_string(4)
        return create_profile_uid(instance)
    return start_unid

def unique_slug_generator(instance,new_slug=None):
    """
    instance of model with slug attr and char(title)
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exist = Klass.objects.filter(slug=slug).exists()
    if qs_exist:
        new_slug = "{}-{}".format(slug=slug,randstr=random_string_generator(4))
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug



   

