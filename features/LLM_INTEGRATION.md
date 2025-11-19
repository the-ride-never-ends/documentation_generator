# LLM Integration for make_gherkins

This document explains how the LLM-powered Gherkin generation works in the `make_gherkins` feature.

## Architecture

The system uses a sophisticated three-LLM pipeline to ensure high-quality Gherkin scenarios:

```
┌─────────────────────────────────────────────────────────────┐
│                    Input: Callable & Docstring               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Generator LLM (GPT-4)                              │
│  - Generates initial Gherkin scenario                       │
│  - Uses docstring context and callable signature            │
│  - Aims for concrete, verifiable assertions                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Classifier LLM (GPT-3.5-turbo)                     │
│  - Evaluates scenario clarity                               │
│  - Checks for vague terms and ambiguous assertions          │
│  - Returns: is_clear (bool) + list of issues               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                 Clear?          Unclear?
                    │               │
                    │               ▼
                    │   ┌─────────────────────────────────┐
                    │   │  Step 3: Editor LLM (GPT-3.5)   │
                    │   │  - Analyzes specific issues     │
                    │   │  - Provides actionable feedback │
                    │   └───────────┬─────────────────────┘
                    │               │
                    │               ▼
                    │   ┌─────────────────────────────────┐
                    │   │  Step 4: Regenerator (GPT-4)    │
                    │   │  - Incorporates feedback        │
                    │   │  - Generates improved scenario  │
                    │   └───────────┬─────────────────────┘
                    │               │
                    │               ▼
                    │       ┌──────────────┐
                    │       │ Loop again?  │
                    │       │ (max iters)  │
                    │       └──────┬───────┘
                    │              │
                    └──────────────┴───────────────────┐
                                                       │
                                                       ▼
                            ┌──────────────────────────────────┐
                            │  Output: Clear Gherkin Scenario  │
                            └──────────────────────────────────┘
```

## LLM Roles

### 1. Generator LLM (GPT-4)
**Model**: `gpt-4`  
**Temperature**: 0.3  
**Purpose**: Generate initial Gherkin scenarios

**System Prompt**:
```
You are an expert at writing clear, specific Gherkin scenarios that describe 
unambiguous, verifiable external behavior. Avoid vague terms like 'executes successfully' - 
instead specify concrete, observable outcomes like 'returns a dictionary with keys: status, data'.
```

**Responsibilities**:
- Generate feature headers with clear user stories
- Create background sections with callable context
- Generate scenarios for: main execution, error handling, examples, verification
- Use concrete assertions and specific data types

### 2. Classifier LLM (GPT-3.5-turbo)
**Model**: `gpt-3.5-turbo`  
**Temperature**: 0.1  
**Purpose**: Evaluate scenario clarity

**System Prompt**:
```
You are a Gherkin quality classifier. You identify vague or ambiguous scenarios 
and require concrete, verifiable assertions.
```

**Evaluation Criteria**:
- ❌ Vague terms: "executes successfully", "works correctly", "is valid"
- ❌ Missing concrete return values or state changes
- ❌ Ambiguous assertions that can't be objectively verified
- ❌ Missing specific data types or formats

**Output Format** (JSON):
```json
{
    "is_clear": true/false,
    "issues": ["list of specific issues found"]
}
```

### 3. Editor LLM (GPT-3.5-turbo)
**Model**: `gpt-3.5-turbo`  
**Temperature**: 0.3  
**Purpose**: Provide actionable feedback

**System Prompt**:
```
You are a Gherkin editor who provides specific, actionable feedback to 
improve scenario clarity.
```

**Feedback Focus**:
- Replace vague terms with concrete assertions
- Add specific data types, formats, or values
- Make assertions objectively verifiable
- Provide specific improvement suggestions

### 4. Regenerator LLM (GPT-4)
**Model**: `gpt-4`  
**Temperature**: 0.3  
**Purpose**: Incorporate feedback and regenerate

**Process**:
- Takes original prompt + editor feedback
- Regenerates scenario with improvements
- Aims to address all identified issues

## Clarity Standards

### ❌ Unclear Examples

```gherkin
Then the function should execute successfully
Then the operation is valid
Then the result is correct
Then appropriate exceptions should be raised
```

### ✅ Clear Examples

```gherkin
Then the function should return a dictionary with keys: status, data, timestamp
Then the function should return an integer between 0 and 100
Then the result should be a list containing exactly 3 string elements
Then a ValueError should be raised with message "invalid input: negative value"
```

## Configuration

### API Key Management

```python
# Option 1: Environment variable
export OPENAI_API_KEY="sk-your-api-key"
gen = GherkinGenerator()

# Option 2: Direct parameter
gen = GherkinGenerator(api_key="sk-your-api-key")

# Option 3: Via convenience function
content, metadata = make_gherkins(func, api_key="sk-your-api-key")
```

### Iteration Control

```python
# Default: 3 iterations per scenario
gen = GherkinGenerator(api_key="sk-...", max_iterations=3)

# Higher quality (more iterations, more API calls)
gen = GherkinGenerator(api_key="sk-...", max_iterations=5)

# Lower cost (fewer iterations, may be less refined)
gen = GherkinGenerator(api_key="sk-...", max_iterations=1)
```

## Error Handling

### Inner Function Errors (RuntimeError)

Inner functions like `_generate_scenario_with_llm`, `_classify_scenario_clarity`, etc. raise `RuntimeError` on failure:

```python
try:
    scenario = self._generate_scenario_with_llm(...)
except RuntimeError as e:
    # Propagates to outer function
    pass
```

### Outer Function Errors (Error Messages)

The main `make_gherkins()` function catches errors and returns them as messages:

```python
content, metadata = make_gherkins(func, api_key="invalid")

# content will be an error message string
# metadata['error'] will contain the error details
# No exception raised
```

Example error metadata:
```python
{
    "error": "Failed to generate Gherkin with LLM: Invalid API key",
    "llm_iterations": 0,
    ...
}
```

## Cost Considerations

### API Calls Per Generation

For a typical function with parameters, return value, and examples:

- Feature header: 1 call (GPT-4)
- Background: 1 call (GPT-4)
- Main scenario: 1 call (GPT-4) + up to max_iterations × 3 calls (GPT-4 + 2×GPT-3.5)
- Error scenario: 1 call (GPT-4) + up to max_iterations × 3 calls (if applicable)
- Examples scenario: 1 call (GPT-4) + up to max_iterations × 3 calls (if applicable)
- Verification scenario: 1 call (GPT-4) + up to max_iterations × 3 calls

**Minimum**: 6 calls (GPT-4)  
**Maximum** (3 iterations, all scenarios): 6 + (4 × 3 × 3) = 42 calls

### Model Costs (OpenAI pricing as of 2024)

- GPT-4: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- GPT-3.5-turbo: ~$0.0005 per 1K input tokens, ~$0.0015 per 1K output tokens

**Estimated cost per generation**: $0.10 - $0.50 depending on iterations and scenario complexity

## Performance

### Typical Generation Time

- Simple function (2 scenarios): ~10-15 seconds
- Complex function (4 scenarios, examples): ~20-40 seconds
- With max refinement (5 iterations): ~30-60 seconds

Times depend on OpenAI API response times and network latency.

## Metadata Tracking

The metadata dictionary includes LLM-specific fields:

```python
{
    "feature_name": "Example Function",
    "callable_name": "example_function",
    "llm_iterations": 8,  # Total iterations across all scenarios
    "num_scenarios": 3,
    "error": None,  # Or error message if failed
    ...
}
```

## Example: Complete Generation Flow

```python
from utils import GherkinGenerator

def divide(a: float, b: float) -> float:
    """Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        float: Result of division
        
    Raises:
        ZeroDivisionError: If b is zero
    """
    return a / b

gen = GherkinGenerator(api_key="sk-...", max_iterations=3)
content, metadata = gen.make_gherkins(divide)

print(f"Generated in {metadata['llm_iterations']} LLM iterations")
print(content)
```

**Output**: Clear Gherkin with specific assertions like:
```gherkin
Then the function should return a float value equal to a divided by b
Then a ZeroDivisionError should be raised with message 'division by zero'
```

Not vague statements like:
```gherkin
Then the function should execute successfully
Then appropriate exceptions should be raised
```

## Best Practices

1. **Start with good docstrings**: Better input → better output
2. **Use reasonable max_iterations**: 3-5 is usually sufficient
3. **Monitor API costs**: Track `llm_iterations` in metadata
4. **Handle errors gracefully**: Check `metadata['error']` field
5. **Validate output**: Always review generated Gherkin before use
6. **Cache results**: Store generated Gherkin to avoid regeneration

## Dependencies

- `openai` package: `pip install openai`
- OpenAI API key with GPT-4 access
- Internet connection for API calls

## Limitations

- Requires valid OpenAI API key
- Depends on external API availability
- Generation time varies with API response
- Costs money per generation
- Quality depends on docstring quality
- No offline/fallback mode
