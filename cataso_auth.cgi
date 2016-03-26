#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use Unicode::Japanese;

sub run {
	%m = ();
	
	if ($in{guestmake}) {
		my $no = int(rand(10000));
		$m{name} = 'guest' . $no;
		$m{pass} = int(rand(10000));
		$id = unpack 'H*', $m{name};
		
		mkdir "./guest/$id" or &error("‚»‚Ì–¼‘O‚Í‚·‚Å‚É“o˜^‚³‚ê‚Ä‚¢‚Ü‚·");
		open my $fh, "> ./guest/$id/user.cgi";
		print $fh "name;$m{name}<>pass;$m{pass}<>\n";
		close $fh;
		
		print qq|Content-type: text/plain; charset=utf-8\n\n|;
		print qq|$m{name}:$m{pass}|;
	} else {
		my $s = Unicode::Japanese->new($in{login_name});
		my $login_name = $s->sjis;
		
		$id   = $in{id} || unpack 'H*', $login_name;
		$pass = $in{pass};
		
		if (-f "$userdir/$id/user.cgi") {
			open my $fh, "< $userdir/$id/user.cgi" or &error("‚»‚Ì‚æ‚¤‚È–¼‘O$in{login_name}‚ÌÌßÚ²Ô°‚ª‘¶Ý‚µ‚Ü‚¹‚ñ");
			my $line = <$fh>;
			close $fh;
			
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				
				if ($k =~ /^y_(.+)$/) {
					$y{$1} = $v;
				}
				else {
					$m{$k} = $v;
				}
			}
			unless ($m{pass} eq $pass) {
				print qq|Status: 404 Not Found\n|;
				return;
			}
			print qq|Content-type: text/plain; charset=utf-8\n\n|;
			
			print qq|$m{cataso_ratio}|;
		} elsif (-f "./guest/$id/user.cgi") {
			open my $fh, "< ./guest/$id/user.cgi" or &error("‚»‚Ì‚æ‚¤‚È–¼‘O$in{login_name}‚ÌÌßÚ²Ô°‚ª‘¶Ý‚µ‚Ü‚¹‚ñ");
			my $line = <$fh>;
			close $fh;
			
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				
				if ($k =~ /^y_(.+)$/) {
					$y{$1} = $v;
				}
				else {
					$m{$k} = $v;
				}
			}
			unless ($m{pass} eq $pass) {
				print qq|Status: 404 Not Found\n|;
				return;
			}
			print qq|Content-type: text/plain; charset=utf-8\n\n|;
			
			print qq|$m{cataso_ratio}|;
		} else {
			print qq|Status: 404 Not Found\n|;
			return;
		}
	}
}

&decode;
&run;
exit;
