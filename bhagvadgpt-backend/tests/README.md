# BhagavadGPT Backend - Test Suite

## Overview

This directory contains all test scripts for the BhagavadGPT backend, including tests for OKF knowledge graph, related field traversal, and various feature implementations.

## Test Categories

### OKF Knowledge Graph Tests (Current - Active)

**Core OKF Tests:**
- `test_okf_complete.py` - Complete OKF system test with statistics
- `test_related_traversal.py` - Basic related field traversal test
- `test_related_detailed.py` - Detailed graph traversal demonstration
- `test_full_integration.py` - End-to-end integration test

**How to run:**
```bash
cd BhagavadGPT/bhagvadgpt-backend
python tests/test_okf_complete.py
python tests/test_related_traversal.py
python tests/test_related_detailed.py
python tests/test_full_integration.py
```

### Legacy Tests (ChromaDB Era - Reference Only)

These tests were created during the ChromaDB implementation and may need updates for OKF:

**Prompt & Integration Tests:**
- `test_main_integration.py` - Main API integration tests
- `test_enhanced_prompt_integration.py` - Enhanced prompt testing
- `test_prompt_deployment.py` - Prompt deployment verification
- `test_okf.py` - Original OKF migration test

**Security & Defense Tests:**
- `test_injection_defense.py` - Prompt injection defense tests
- `test_response_length.py` - Response length validation
- `test_response_length_functional.py` - Functional response length tests

**Checkpoint Tests:**
- `test_checkpoint_manual.py` - Manual checkpoint verification
- `run_checkpoint_tests.py` - Automated checkpoint test runner
- `test_cases_checkpoint.json` - Test cases data

**Startup Tests:**
- `test_startup.py` - Backend startup verification

## Quick Test Commands

### Test OKF Knowledge Graph
```bash
python tests/test_okf_complete.py
```

### Test Related Field Traversal
```bash
python tests/test_related_traversal.py
python tests/test_related_detailed.py
```

### Full Integration Test
```bash
python tests/test_full_integration.py
```

### Run All Current Tests
```bash
cd tests
python test_okf_complete.py
python test_related_traversal.py
python test_related_detailed.py
python test_full_integration.py
```

## Test Data

- `test_cases_checkpoint.json` - Test case definitions for checkpoint testing

## Expected Results

All OKF tests should show:
- ✅ 700 verses loaded
- ✅ 676 verses with tags (96.6%)
- ✅ 297 verses with related connections (42.4%)
- ✅ Graph traversal working
- ✅ Token limits respected

## Documentation

For detailed testing instructions, see:
- `../docs/TESTING_GUIDE.md` - Complete testing guide
- `../docs/OKF_RELATED_FIELD.md` - Related field feature docs
- `../docs/KNOWLEDGE_GRAPH_IMPLEMENTATION.md` - Implementation details

## Notes

- Legacy tests may require updates to work with the current OKF implementation
- Focus on the "Current - Active" tests for OKF knowledge graph validation
- All test paths are relative to the backend root directory
