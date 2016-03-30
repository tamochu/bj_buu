(function(){ 
    
    
    // see
    // https://developer.mozilla.org/ja/docs/Web/JavaScript/Base64_encoding_and_decoding
    function base64DecToArr (sBase64, nBlocksSize) {
 
        var
            sB64Enc = sBase64.replace(/[^A-Za-z0-9\+\/]/g, ""), nInLen = sB64Enc.length,
            nOutLen = nBlocksSize ? Math.ceil((nInLen * 3 + 1 >> 2) / nBlocksSize) * nBlocksSize : nInLen * 3 + 1 >> 2, taBytes = new Uint8Array(nOutLen);
 
        for (var nMod3, nMod4, nUint24 = 0, nOutIdx = 0, nInIdx = 0; nInIdx < nInLen; nInIdx++) {
            nMod4 = nInIdx & 3;
            nUint24 |= b64ToUint6(sB64Enc.charCodeAt(nInIdx)) << 18 - 6 * nMod4;
            if (nMod4 === 3 || nInLen - nInIdx === 1) {
                for (nMod3 = 0; nMod3 < 3 && nOutIdx < nOutLen; nMod3++, nOutIdx++) {
                    taBytes[nOutIdx] = nUint24 >>> (16 >>> nMod3 & 24) & 255;
                }
                nUint24 = 0;
            }
        }
        return taBytes.buffer;
    }
        
    function b64ToUint6 (nChr) {
 
        return nChr > 64 && nChr < 91 ?
            nChr - 65
            : nChr > 96 && nChr < 123 ?
              nChr - 71
            : nChr > 47 && nChr < 58 ?
              nChr + 4
            : nChr === 43 ?
              62
            : nChr === 47 ?
              63
            :
              0;
    }
 
    // see Corodva
 
    var b64_6bit = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var b64_12bit;
 
    var b64_12bitTable = function() {
        b64_12bit = [];
        for (var i=0; i<64; i++) {
            for (var j=0; j<64; j++) {
                b64_12bit[i*64+j] = b64_6bit[i] + b64_6bit[j];
            }
        }
        b64_12bitTable = function() { return b64_12bit; };
        return b64_12bit;
    };
 
    function uint8ToBase64(rawData) {
        var numBytes = rawData.byteLength;
        var output="";
        var segment;
        var table = b64_12bitTable();
        for (var i=0;i<numBytes-2;i+=3) {
            segment = (rawData[i] << 16) + (rawData[i+1] << 8) + rawData[i+2];
            output += table[segment >> 12];
            output += table[segment & 0xfff];
        }
        if (numBytes - i == 2) {
            segment = (rawData[i] << 16) + (rawData[i+1] << 8);     
            output += table[segment >> 12];
            output += b64_6bit[(segment & 0xfff) >> 6];
            output += '=';
        } else if (numBytes - i == 1) {
            segment = (rawData[i] << 16);
            output += table[segment >> 12];
            output += '==';
        }
        return output;
    }
 
 
    
    
    window.b64utils = {
        decode : base64DecToArr ,
        encode : uint8ToBase64
    };
    
 
})();