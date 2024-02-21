# Rule authoring

All the rules for validating cpg datasets are encapsulated in a single class
that inherits the `BaseRule` class defined in `cpg.rule.BaseRule`.

`BaseRule` expects a `validate` to method to be defined by the rule author.
The validate method gets a polars `polars.Lazyframe` as input and returns a `bool`
indicating the result of the validation. The body of the `validate` method is usually
just a chain of dataframe operations. If the validation fails, then the `validate`
method is expected to write a dataframe as parquet file to disk containing all the
rows that failed the validation.

The `validate` method has no other expected structure, but we have come up with a
few patterns that can help with performance and code readability.

## Use a chain rather than defining new variables for each step

```python
df = (
    df
    .filter()
    .filter()
    .select()
    .collect()
)

```

## Use filtering to get to the failing rows and not the other way around

```python
df = (
    df
    .filter()
    .filter()
    .select()
    .collect()
)

```

## Always add a `select` at the end of the chain and only select for keys

```python
df = (
    df
    .filter()
    .filter()
    .select()
    .collect()
)

```

