import inspect

stack = inspect.stack()
calling_context = next(context for context in stack if context.filename != __file__)
print(calling_context.filename)