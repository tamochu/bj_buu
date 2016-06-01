package TestCUI;

require './TestFramework/TestInterface.pm';
require './TestFramework/TestResultCUI.pm';

my $test_result = TestResultCUI->new();
my $test_interface = TestInterface->new($test_result);
$test_interface->run_test("./TestFramework/Tests/TestAccessor.pm");
$test_interface->output_result();

