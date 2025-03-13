'''Module for testing inheritance documentation.

This module contains a class hierarchy to test inheritance documentation.
'''

class BaseClass:
    '''Base class with multiple methods and properties.
    
    This class defines methods and properties that will be inherited.
    
    Attributes:
        base_attr: A base attribute defined in the parent class.
    '''
    
    base_attr = "base value"
    
    def __init__(self, value: str):
        '''Initialize the base class.
        
        Args:
            value: Initial value for the instance.
        '''
        self._value = value
    
    @property
    def value(self) -> str:
        '''Get the value property.
        
        Returns:
            The current value.
        '''
        return self._value
    
    def base_method(self, param: int) -> str:
        '''A method in the base class.
        
        Args:
            param: An integer parameter.
            
        Returns:
            A string result.
        '''
        return f"{self._value}: {param}"
    
    def overridable_method(self) -> str:
        '''A method that will be overridden in child classes.
        
        Returns:
            A string message.
        '''
        return "Base implementation"


class ChildClass(BaseClass):
    '''Child class that inherits from BaseClass.
    
    This class demonstrates single inheritance.
    
    Attributes:
        child_attr: An attribute specific to the child class.
    '''
    
    child_attr = "child value"
    
    def __init__(self, value: str, extra: str):
        '''Initialize the child class.
        
        Args:
            value: Initial value passed to base class.
            extra: Extra value specific to child class.
        '''
        super().__init__(value)
        self._extra = extra
    
    def child_method(self) -> str:
        '''A method specific to the child class.
        
        Returns:
            A string result.
        '''
        return f"{self._value} + {self._extra}"
    
    def overridable_method(self) -> str:
        '''Override the method from BaseClass.
        
        Returns:
            A different string message.
        '''
        return f"Child implementation: {super().overridable_method()}"


class GrandchildClass(ChildClass):
    '''Grandchild class that inherits from ChildClass.
    
    This demonstrates multi-level inheritance.
    '''
    
    def grandchild_method(self) -> str:
        '''A method specific to the grandchild.
        
        Returns:
            A string result using methods from parent classes.
        '''
        return f"Grand: {self.child_method()}"
    
    def overridable_method(self) -> str:
        '''Override the method again.
        
        Returns:
            An even more different message.
        '''
        return f"Grandchild implementation: {super().overridable_method()}"


class MultipleParentsBase1:
    '''First base class for multiple inheritance.'''
    
    def base1_method(self) -> str:
        '''Method from first base.
        
        Returns:
            A string message.
        '''
        return "Base1"


class MultipleParentsBase2:
    '''Second base class for multiple inheritance.'''
    
    def base2_method(self) -> str:
        '''Method from second base.
        
        Returns:
            A string message.
        '''
        return "Base2"
    
    def common_method(self) -> str:
        '''A method that exists in both bases.
        
        Returns:
            A string from Base2.
        '''
        return "Common from Base2"


class MultipleParentsBase3:
    '''Third base class for multiple inheritance.'''
    
    def base3_method(self) -> str:
        '''Method from third base.
        
        Returns:
            A string message.
        '''
        return "Base3"
    
    def common_method(self) -> str:
        '''A method that exists in both bases.
        
        Returns:
            A string from Base3.
        '''
        return "Common from Base3"


class MultipleInheritanceClass(MultipleParentsBase1, MultipleParentsBase2, MultipleParentsBase3):
    '''Class that inherits from multiple parent classes.
    
    This demonstrates complex multiple inheritance with method resolution order.
    '''
    
    def child_method(self) -> str:
        '''Child's own method.
        
        Returns:
            A string message.
        '''
        return "Child's method"
