package jcode;
&init unless defined $version;
sub init {
    $version =  '2.13:SmallEdition1.1';
    $convf{'jis'} = *jis2sjis;
    $convf{'euc'} = *euc2sjis;
    $convf{'sjis'} = *sjis2sjis;
}
sub getcode {
    local(*s) = @_;
    local($code);
    if ($s !~ /[\e\200-\377]/) {	# not Japanese
	$matched = 0;
	$code = undef;
    }					# 'jis'
    elsif ($s =~ /\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I/o) {
	$code = 'jis';
    }
    elsif ($s =~ /[\000-\006\177\377]/o) {	# 'binary'
	$code = 'binary';
    }
    else {				# should be 'euc' or 'sjis'
	local($sjis, $euc) = (0, 0);

	while ($s =~ /(([\201-\237\340-\374][\100-\176\200-\374])+)/go) {
	    $sjis += length($1);
	}
	while ($s =~ /(([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])+)/go) {
	    $euc  += length($1);
	}
	&max($sjis, $euc);
	$code = ('euc', undef, 'sjis')[($sjis<=>$euc) + $[ + 1];
    }
    $code;
}
sub max { $_[ $[ + ($_[ $[ ] < $_[ $[ + 1 ]) ]; }
sub convert {
    local(*s, $ocode, $icode, $opt) = @_;
    return (undef, undef) unless $icode = $icode || &getcode(*s);
    return (undef, $icode) if $icode eq 'binary';
    local(*f) = $convf{$icode};
    &f(*s);
     (*f);
}
sub jis2sjis {
    local(*s, $n) = @_;
    &jis2jis(*s, $opt) if $opt;
    $s =~ s/(\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I)([^\e]*)/&_jis2sjis($1,$2)/geo;
    $n;
}
sub _jis2sjis {
    local($esc, $s) = @_;
    if ($esc =~ /^\e\$\(D/o) {
	$s =~ s/../\x81\xac/g;
	$n = length;
    }
    elsif ($esc !~ /^\e\([BJ]/o) {
	$n += $s =~ tr/\041-\176/\241-\376/;
	if ($esc =~ /^\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D/o) {
	    $s =~ s/([\241-\376][\241-\376])/&e2s($1)/geo;
	}
    }
    $s;
}
sub euc2sjis {
    local(*s, $n) = @_;
    $n = $s =~ s/([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])/&e2s($1)/geo;
}
sub e2s {
    local($c1, $c2, $code);
    ($c1, $c2) = unpack('CC', $code = shift);

    if ($c1 == 0x8e) {		# SS2
	return substr($code, 1, 1);
    } elsif ($c1 == 0x8f) {	# SS3
	return "\x81\xac";
    } elsif ($c1 % 2) {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x31 : 0x71);
	$c2 -= 0x60 + ($c2 < 0xe0);
    } else {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x30 : 0x70);
	$c2 -= 2;
    }
    if ($cache) {
	$e2s{$code} = pack('CC', $c1, $c2);
    } else {
	pack('CC', $c1, $c2);
    }
}
sub sjis2sjis {
    local(*s,) = @_;
}
1;
