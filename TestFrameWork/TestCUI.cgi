#!/usr/local/bin/perl --
package TestCUI;

require './TestFramework/TestInterface.pm';
require './TestFramework/TestResultCUI.pm';

my $test_result = TestResultCUI->new();
my $test_interface = TestInterface->new($test_result);
#$test_interface->run_test("./TestFramework/Tests/samples/sample_test.t");
#$test_interface->run_test("./TestFramework/Controller/Accessor/TestAccessor.pm");
$test_interface->run_test("./TestFramework/Controller/TestController.pm");
$test_interface->output_result();
$test_interface->restore_data();

