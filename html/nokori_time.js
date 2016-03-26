function nokori_time_jinro(now_time) {
	if (now_time > 0) {
		min = Math.floor(now_time / 60);
		sec = Math.floor(now_time % 60);
		sec = ("00" + sec).substr(("00" + sec).length-2, 2);
		nokori = '<FONT size="+2">' + min + '</FONT>' + 'ï™' + '<FONT size="+2">' + sec + '</FONT>' + 'ïb';
		document.getElementById("nokori_time").innerHTML = nokori;
		next_time = now_time - 1;
		setTimeout("nokori_time_jinro(next_time)",1000);
	}
	else {
		document.getElementById("nokori_time").innerHTML = '<font color="#FF0000"><b>ìäï[ÇµÇƒÇ≠ÇæÇ≥Ç¢<b></font>';
	}
}

function nokori_time(now_time, r_time, gacha_rest, gacha2_rest, offertory_rest) {
	if (now_time >= 0) {
		hour = Math.floor(now_time / 3600);
		min  = Math.floor(now_time % 3600 / 60);
		sec  = Math.floor(now_time % 60);
		min  = ("00" + min).substr(("00" + min).length-2, 2);
		sec  = ("00" + sec).substr(("00" + sec).length-2, 2);
		nokori = min + 'ï™' + sec + 'ïb';
		if (hour > 0) {
			nokori = hour + 'éû' + nokori;
		}
		try {
			document.getElementById("nokori_time").innerHTML = nokori;
		} catch (e) {
		}
	} else {
			document.getElementById("nokori_time").innerHTML = '<font color="#FF0000"><b>ÇnÇjÅI<b></font>';
	}
	if (r_time > 0) {
		rhour = Math.floor(r_time / 3600);
		rmin  = Math.floor(r_time % 3600 / 60);
		rsec  = Math.floor(r_time % 60);
		rmin  = ("00" + rmin).substr(("00" + rmin).length-2, 2);
		rsec  = ("00" + rsec).substr(("00" + rsec).length-2, 2);
		rest = rhour + 'éûä‘' + rmin + 'ï™' + rsec + 'ïbå„';
		try {
			document.getElementById("reset_time").innerHTML = rest;
		} catch (e) {
		}
	}
	else {
		try {
			document.getElementById("reset_time").innerHTML = '<font color="#FF0000"><b>äJêÌÅI<b></font>';
		} catch (e) {
		}
	}
	if (gacha_rest >= 0) {
		ghour = Math.floor(gacha_rest / 3600);
		gmin  = Math.floor(gacha_rest % 3600 / 60);
		gsec  = Math.floor(gacha_rest % 60);
		gmin  = ("00" + gmin).substr(("00" + gmin).length-2, 2);
		gsec  = ("00" + gsec).substr(("00" + gsec).length-2, 2);
		gnokori = gmin + 'ï™' + gsec + 'ïb';
		if (ghour > 0) {
			gnokori = ghour + 'éû' + gnokori;
		}
		try {
			document.getElementById("gacha_time").innerHTML = gnokori;
		} catch (e) {
		}
	}
	if (gacha2_rest >= 0) {
		g2hour = Math.floor(gacha2_rest / 3600);
		g2min  = Math.floor(gacha2_rest % 3600 / 60);
		g2sec  = Math.floor(gacha2_rest % 60);
		g2min  = ("00" + g2min).substr(("00" + g2min).length-2, 2);
		g2sec  = ("00" + g2sec).substr(("00" + g2sec).length-2, 2);
		g2nokori = g2min + 'ï™' + g2sec + 'ïb';
		if (g2hour > 0) {
			g2nokori = g2hour + 'éû' + g2nokori;
		}
		try {
			document.getElementById("gacha_time2").innerHTML = g2nokori;
		} catch (e) {
		}
	}
	if (offertory_rest >= 0) {
		ohour = Math.floor(offertory_rest / 3600);
		omin  = Math.floor(offertory_rest % 3600 / 60);
		osec  = Math.floor(offertory_rest % 60);
		omin  = ("00" + omin).substr(("00" + omin).length-2, 2);
		osec  = ("00" + osec).substr(("00" + osec).length-2, 2);
		onokori = omin + 'ï™' + osec + 'ïb';
		if (ohour > 0) {
			onokori = ohour + 'éû' + onokori;
		}
		try {
			document.getElementById("offertory_time").innerHTML = onokori;
		} catch (e) {
		}
	}

	next_time = now_time - 1;
	next_rest = r_time - 1;
	next_gacha = gacha_rest - 1;
	next_gacha2 = gacha2_rest - 1;
	next_offertory = offertory_rest - 1;
	if (next_time >= -1 || next_rest >= -1 || next_gacha >= -1 || next_gacha2 >= -1 || next_offertory >= -1) {
		setTimeout("nokori_time(next_time, next_rest, next_gacha, next_gacha2, next_offertory)",1000);
	}
}
