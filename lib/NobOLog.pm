#!/usr/local/bin/perl --
package NobOLog;
use strict;
use warnings;
use JSON qw/decode_json/;
use NobOConfig;

sub new {
	my $clazz = shift;
	my $self = {
		Text => '',
		ToName => ''
	};
	return bless $self, $clazz;
}

sub text {
	my $self = shift;
	if (@_) {
		$self->{Text} = shift;
	}
	return $self->{Text};
}

sub toName {
	my $self = shift;
	if (@_) {
		$self->{ToName} = shift;
	}
	return $self->{ToName};
}

# accessor ‚±‚±‚Ü‚Å
sub appendText {
	my $self = shift;
	my $add = shift;
	$self->text($self->text() . $add);
}

sub sendMail {
	my $self = shift;
	my %config = NobOConfig->getConfig();
	
	my $userdir = $config{userdir};
	
	if ($self->toName() eq '') {
		$self->error('no name');
		return;
	}
	my $send_id = $self->toName();
	
	my $this_file = "$userdir/$send_id/nobo_letter.cgi";
	unless (-f "$this_file") {
		open my $fh, "> $this_file" or return;
		close $fh;
	}
	
	if ($self->text() eq '') {
		$self->error('no text');
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_file" or return;
	eval { flock $fh, 2; };
	
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	my $mname = 'ƒVƒXƒeƒ€';
	my $text = $self->text();
	my $time = time();
	my($min,$hour,$mday,$mon,$year) = (localtime($time))[1..4];
	my $date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
	unshift @lines, "$time<>$date<>$mname<>0<><><>$text<><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

sub error {
	my $self = shift;
	my $text = shift;
	
	open my $fh, ">> ./log/error.cgi";
	print $fh "$text\n\n\n";
	close $fh;
	
}

sub TO_JSON {
	my $self = shift;
	my %h_self = map { $_ => $self->{$_} } keys(%$self);

	return { ref($self) => \%h_self };
}

sub FROM_JSON {
	my $self = shift;
	my $json = shift;
	
	my $data = decode_json($json);
	for my $key (keys(%$self)) {
		$self->{$key} = ${${$data}{NobOArmy}}{$key};
	}
}

1;