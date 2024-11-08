use pyo3::{
    exceptions::PyValueError,
    types::PyModuleMethods,
    prelude::{pyfunction, pymodule, wrap_pyfunction, PyModule, PyResult, Python, Bound},
};
use std::collections::HashMap;
use std::fmt;

use pest::{Parser, Token};
use pest_derive::Parser;

#[derive(Parser)]
#[grammar = "key_parser.pest"]
pub struct KeyParser;

impl fmt::Display for Rule {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt::Debug::fmt(self, f)
    }
}

/// Parse S3 prefixs in Cell painting gallery.
///
/// * `prefix`: S3 prefix as a string
#[pyfunction]
fn parse_prefix(prefix: String) -> PyResult<HashMap<String, String>> {
    let mut token_pos0: HashMap<String, usize> = HashMap::new();
    let mut parsed_prefix: HashMap<String, String> = HashMap::new();
    let key = KeyParser::parse(Rule::key, &prefix);
    match key {
        Ok(key) => {
            let key_tokens = key.tokens();
            for token in key_tokens {
                match token {
                    Token::Start { rule, pos } => {
                        token_pos0.insert(rule.to_string(), pos.pos());
                    }
                    Token::End { rule, pos } => {
                        if let Some((_, v)) = token_pos0.remove_entry(&rule.to_string()) {
                            let value: String = (&prefix[v..pos.pos()]).into();
                            parsed_prefix.insert(rule.to_string(), value);
                        }
                    }
                }
            }
            return Ok(parsed_prefix);
        }
        Err(e) => return Err(PyValueError::new_err(e.to_string())),
    }
}

#[pyfunction]
fn parse_prefix_allow_threads(py: Python<'_>, prefix: String) -> PyResult<HashMap<String, String>> {
    py.allow_threads(|| parse_prefix(prefix))
}

/// A Python module implemented in Rust.
#[pymodule]
fn cpgparser(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_prefix, m)?)?;
    m.add_function(wrap_pyfunction!(parse_prefix_allow_threads, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::parse_prefix;

    #[test]
    fn check_smaple_001() {
        let prefix: String = "cpg0000-jump-pilot/source_4/images/2020_11_04_CPJUMP1/illum/BR00116991/BR00116991_IllumHighZBF.npy".to_string();
        let _ = parse_prefix(prefix);
        // assert_eq!()
    }

    #[test]
    fn check_smaple_002() {
        let prefix: String = "cpg0037-oasis/axiom/workspace/scratch/prod_25/plate_41002688/biochem.parquet".to_string();
        let res = parse_prefix(prefix);
        println!("{:?}", res);
        // assert_eq!()
    }
}
