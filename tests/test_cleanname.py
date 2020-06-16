# encoding: utf-8
import pytest
from cleanco import prepare_terms, basename


@pytest.fixture
def terms():
   return prepare_terms()

# Tests that demonstrate stuff is stripped away

basic_cleanup_tests = {
   "name w/ suffix":           "Hello World Oy",
   "name w/ ', ltd.'":         "Hello World, ltd.",
   "name w/ ws suffix ws":     "Hello    World ltd",
   "name w/ suffix ws":        "Hello World ltd ",
   "name w/ suffix dot ws":    "Hello World ltd. ",
   "name w/ ws suffix dot ws": " Hello World ltd. ",
}

def test_basic_cleanups(terms):
   expected = "Hello World"
   errmsg = "cleanup of %s failed"
   for testname, variation in basic_cleanup_tests.items():
      assert basename(variation, terms) == expected, errmsg % testname

multi_cleanup_tests = {
   "name + suffix":          "Hello World Oy",
   "name + suffix (without punct)":          "Hello World sro",
   "prefix + name":          "Oy Hello World",
   "prefix + name + suffix": "Oy Hello World Ab",
   "name w/ term in middle": "Hello Oy World",
   "name w/ complex term in middle": "Hello pty ltd World",
   "name w/ mid + suffix":   "Hello Oy World Ab"
}

def test_multi_type_cleanups(terms):
   expected = "Hello World"
   errmsg = "cleanup of %s failed"
   for testname, variation in multi_cleanup_tests.items():
      result = basename(variation, terms, prefix=True, suffix=True, middle=True)
      assert result == expected, errmsg % testname


# Tests that demonstrate basename can be run twice effectively

double_cleanup_tests = {
   "name + two prefix":      "Ab Oy Hello World",
   "name + two suffix":      "Hello World Ab Oy",
   "name + two in middle":   "Hello Ab Oy World"
}

def test_double_cleanups(terms):
   expected = "Hello World"
   errmsg = "cleanup of %s failed"
   for testname, variation in multi_cleanup_tests.items():
      result = basename(variation, terms, prefix=True, suffix=True, middle=True)
      final = basename(result, terms, prefix=True, suffix=True, middle=True)

      assert final == expected, errmsg % testname

# Tests that demonstrate organization name is kept intact

preserving_cleanup_tests = {
   "name with comma": ("Hello, World, ltd.", "Hello, World"),
   "name with dot": ("Hello. World, Oy", "Hello. World")
}

def test_preserving_cleanups(terms):
   errmsg = "preserving cleanup of %s failed"
   for testname, (variation, expected) in preserving_cleanup_tests.items():
      assert basename(variation, terms) == expected, errmsg % testname

# Test umlauts


unicode_umlaut_tests = {
   "name with umlaut in end": ("Säätämö Oy", "Säätämö"),
   "name with umlauts & comma": ("Säätämö, Oy", "Säätämö"),
   "name with no ending umlaut": ("Säätämo Oy", "Säätämo"),
   "name with beginning umlaut": ("Äätämo Oy", "Äätämo"),
   "name with just umlauts": ("Äätämö", "Äätämö"),
   "cyrillic name": ("ОАО Новороссийский морской торговый порт", "Новороссийский морской торговый порт")

}

def test_with_unicode_umlauted_name(terms):
   errmsg = "preserving cleanup of %s failed"
   for testname, (variation, expected) in unicode_umlaut_tests.items():
      assert basename(variation, terms, prefix=True) == expected, errmsg % testname


def test_deterministic_cleanup_for_two_types(terms):
   assert basename("name ltd inc.", terms, prefix=False, suffix=True, middle=False) == "name"
   assert basename("name inc. ltd", terms, prefix=False, suffix=True, middle=False) == "name inc."


terms_with_accents_tests = {
   "term with ł correct spelling": ("Łoś spółka z o.o", "Łoś"),
   "term with ł incorrect spelling": ("Łoś spolka z o.o", "Łoś"),
}

def test_terms_with_accents(terms):
   errmsg = "preserving cleanup of %s failed"
   for testname, (variation, expected) in terms_with_accents_tests.items():
      assert basename(variation, terms, suffix=True) == expected, errmsg % testname
