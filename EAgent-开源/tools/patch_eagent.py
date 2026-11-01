#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAgent-文心 (Wenxin fork) binary patcher.

Takes an UNMODIFIED EAgent release EXE and produces the Wenxin-forked EXE by
applying only EQUAL-LENGTH byte replacements, so the PE layout stays intact.

Usage:
    python patch_eagent.py <in.exe> <out.exe>

Every replacement is byte-for-byte the same length as the original, therefore
the file size never changes and the 易语言 runtime / embedded PowerShell scripts
keep working.
"""
import sys

GBK = "百度文心".encode("gbk")            # 8 bytes  == len("DeepSeek")
URL_OLD = b"https://chat.deepseek.com"     # 25 bytes
URL_NEW = b"https://wenxin.baidu.com/"     # 25 bytes
PROF_OLD = b"deepseek_debug_profile"       # 22 bytes
PROF_NEW = b"wenxin___debug_profile"       # 22 bytes
RE_OLD = b"chat\\.deepseek\\.com"          # 19 bytes
RE_NEW = b"wenxin\\.baidu\\.com."          # 19 bytes

SELECTORS_NEW = """$Selectors = @{
    assistant = @('.answer-box')
    user      = @('[class*="answer-ask"]')
    input     = @('#chat-textarea','textarea')
    sendBtn   = @('#ci-submit-button-ai','.ci-submit-button-ai-active')
}
""".encode("utf-8")

LASTASSIST_JS = (
    "(function(){var a=pick('assistant'),e=a.pop(),t=(e&&e.innerText)||'';"
    "return(t.length>5&&!/^正在/.test(t))?t:'';})()"
).encode("utf-8")


def replace_selectors(d):
    s = d.find(b"$Selectors")
    j = d.find(b"$SelJson", s)
    if s < 0 or j < 0:
        raise RuntimeError("selectors block not found")
    region = d[s:j]
    pad = len(region) - len(SELECTORS_NEW) - 2
    if pad < 0:
        raise RuntimeError("selectors block too small for replacement")
    return d[:s] + SELECTORS_NEW + b" " * pad + b"\r\n" + d[j:]


def replace_lastassist(d):
    i = d.find(b"$lastAssistJs =")
    if i < 0:
        raise RuntimeError("$lastAssistJs definition not found")
    a = d.find(b'@"', i)
    st = a + 2
    e = d.find(b'"@', st)
    old_len = e - st
    if len(LASTASSIST_JS) + 2 > old_len:
        raise RuntimeError("lastAssistJs block too small")
    inner = b"\n" + LASTASSIST_JS + b" " * (old_len - len(LASTASSIST_JS) - 2) + b"\n"
    return d[:st] + inner + d[e:]


def patch(d):
    n0 = len(d)
    if d.count(URL_OLD) != 1:
        raise RuntimeError("expected exactly one DeepSeek URL")
    d = d.replace(URL_OLD, URL_NEW)                 # 1) page URL
    d = d.replace(b"DeepSeek", GBK)                 # 2) UI text / window title (8)
    for phrase in (b"\xcf\xf2deepseek\xb7\xa2\xcb\xcd\xce\xc4\xb1\xbe",   # 向deepseek发送文本
                   b"\xd3\xc0\xd4\xb6\xb2\xbb\xd2\xaa\xb0\xd1deepseek\xb4\xb0\xbf\xda\xb9\xd8\xb5\xf4"):
        if phrase in d:
            d = d.replace(phrase, phrase.replace(b"deepseek", GBK))
    d = d.replace(PROF_OLD, PROF_NEW)               # 3) isolated browser profile
    if d.count(RE_OLD) == 1:
        d = d.replace(RE_OLD, RE_NEW)               # 4) CDP page match regex
    d = replace_selectors(d)                        # 5) Wenxin DOM selectors
    d = replace_lastassist(d)                       # 6) ignore "正在思考" placeholder
    if len(d) != n0:
        raise RuntimeError("length changed -> layout would break")
    return d


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    data = open(src, "rb").read()
    out = patch(data)
    open(dst, "wb").write(out)
    print("patched -> %s (%d bytes)" % (dst, len(out)))


if __name__ == "__main__":
    main()
