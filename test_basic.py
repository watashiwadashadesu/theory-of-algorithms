"""
Простой тест для проверки основных функций PRF Constructor.
"""

from core.prf import Zero, Successor, Projection, create_addition, create_multiplication, create_factorial
from core.evaluator import Evaluator
from core.validator import Validator


def test_basic_functions():
    """Тестирует базовые функции."""
    print("Тестирование базовых функций...")
    
    # Тест Zero
    z = Zero()
    assert z.evaluate([5]) == 0, "Zero function failed"
    print("✓ Zero function works")
    
    # Тест Successor
    s = Successor()
    assert s.evaluate([5]) == 6, "Successor function failed"
    print("✓ Successor function works")
    
    # Тест Projection
    p = Projection(3, 2)
    assert p.evaluate([1, 2, 3]) == 2, "Projection function failed"
    print("✓ Projection function works")


def test_addition():
    """Тестирует функцию сложения."""
    print("\nТестирование сложения...")
    add = create_addition()
    
    # Проверка арности
    assert add.arity() == 2, f"Addition arity should be 2, got {add.arity()}"
    
    # Тесты вычисления
    evaluator = Evaluator()
    result = evaluator.evaluate(add, [0, 5])
    assert result == 5, f"add(0, 5) should be 5, got {result}"
    print(f"✓ add(0, 5) = {result}")
    
    result = evaluator.evaluate(add, [3, 4])
    assert result == 7, f"add(3, 4) should be 7, got {result}"
    print(f"✓ add(3, 4) = {result}")


def test_multiplication():
    """Тестирует функцию умножения."""
    print("\nТестирование умножения...")
    mult = create_multiplication()
    
    # Проверка арности
    assert mult.arity() == 2, f"Multiplication arity should be 2, got {mult.arity()}"
    
    # Тесты вычисления
    evaluator = Evaluator()
    result = evaluator.evaluate(mult, [0, 5])
    assert result == 0, f"mult(0, 5) should be 0, got {result}"
    print(f"✓ mult(0, 5) = {result}")
    
    result = evaluator.evaluate(mult, [3, 4])
    assert result == 12, f"mult(3, 4) should be 12, got {result}"
    print(f"✓ mult(3, 4) = {result}")


def test_factorial():
    """Тестирует функцию факториала."""
    print("\nТестирование факториала...")
    fact = create_factorial()
    
    # Проверка арности
    assert fact.arity() == 1, f"Factorial arity should be 1, got {fact.arity()}"
    
    # Тесты вычисления
    evaluator = Evaluator()
    result = evaluator.evaluate(fact, [0])
    assert result == 1, f"fact(0) should be 1, got {result}"
    print(f"✓ fact(0) = {result}")
    
    result = evaluator.evaluate(fact, [5])
    assert result == 120, f"fact(5) should be 120, got {result}"
    print(f"✓ fact(5) = {result}")


def test_validation():
    """Тестирует валидацию."""
    print("\nТестирование валидации...")
    
    add = create_addition()
    errors = Validator.validate(add)
    assert len(errors) == 0, f"Addition should be valid, got errors: {errors}"
    print("✓ Addition validation passed")
    
    is_valid = Validator.is_valid(add)
    assert is_valid, "Addition should be valid"
    print("✓ Addition is_valid check passed")


def test_serialization():
    """Тестирует сериализацию функций."""
    print("\nТестирование сериализации...")
    
    from core.prf import function_from_dict
    
    add = create_addition()
    func_dict = add.to_dict()
    
    # Восстанавливаем функцию
    restored = function_from_dict(func_dict)
    
    # Проверяем, что она работает так же
    evaluator = Evaluator()
    original_result = evaluator.evaluate(add, [3, 4])
    restored_result = evaluator.evaluate(restored, [3, 4])
    
    assert original_result == restored_result, "Serialization failed"
    print("✓ Serialization works correctly")


if __name__ == "__main__":
    try:
        test_basic_functions()
        test_addition()
        test_multiplication()
        test_factorial()
        test_validation()
        test_serialization()
        
        print("\n" + "="*50)
        print("Все тесты пройдены успешно! ✓")
        print("="*50)
    
    except AssertionError as e:
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

