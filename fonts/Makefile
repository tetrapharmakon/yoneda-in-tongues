GITHUB := https://github.com/notofonts

# Noto font versions (update these to bump)
NOTO_LGC_SERIF_VER := NotoSerif-v2.015
NOTO_LGC_SANS_VER := NotoSans-v2.015
NOTO_CJK_SERIF_VER := Serif2.003
NOTO_ARABIC_VER := NotoNaskhArabic-v2.021
NOTO_HEBREW_VER := NotoSerifHebrew-v2.004
NOTO_DEVANAGARI_VER := NotoSerifDevanagari-v2.006
NOTO_THAI_VER := NotoSerifThai-v2.002
NOTO_GEORGIAN_VER := NotoSerifGeorgian-v2.003

LGC_STYLES := Regular Bold Italic BoldItalic
CJK_STYLES := Regular Bold
SCRIPT_STYLES := Regular Bold

NOTO_FONTS := \
	$(foreach s,$(LGC_STYLES),NotoSerif-$(s).ttf) \
	$(foreach s,$(LGC_STYLES),NotoSans-$(s).ttf) \
	$(foreach s,$(CJK_STYLES),NotoSerifJP-$(s).otf) \
	$(foreach s,$(CJK_STYLES),NotoSerifSC-$(s).otf) \
	$(foreach s,$(CJK_STYLES),NotoSerifKR-$(s).otf) \
	$(foreach s,$(SCRIPT_STYLES),NotoNaskhArabic-$(s).ttf) \
	$(foreach s,$(SCRIPT_STYLES),NotoSerifHebrew-$(s).ttf) \
	$(foreach s,$(SCRIPT_STYLES),NotoSerifDevanagari-$(s).ttf) \
	$(foreach s,$(SCRIPT_STYLES),NotoSerifThai-$(s).ttf) \
	$(foreach s,$(SCRIPT_STYLES),NotoSerifGeorgian-$(s).ttf)

all: $(NOTO_FONTS)

# Latin/Greek/Cyrillic fonts (hinted/ttf variants)
$(foreach s,$(LGC_STYLES),NotoSerif-$(s).ttf): NotoSerif-%.ttf:
	curl -sL $(GITHUB)/latin-greek-cyrillic/releases/download/$(NOTO_LGC_SERIF_VER)/$(NOTO_LGC_SERIF_VER).zip -o /tmp/NotoSerif.zip
	unzip -j -o /tmp/NotoSerif.zip "*/hinted/ttf/NotoSerif-$*.ttf" -d .
	rm /tmp/NotoSerif.zip

$(foreach s,$(LGC_STYLES),NotoSans-$(s).ttf): NotoSans-%.ttf:
	curl -sL $(GITHUB)/latin-greek-cyrillic/releases/download/$(NOTO_LGC_SANS_VER)/$(NOTO_LGC_SANS_VER).zip -o /tmp/NotoSans.zip
	unzip -j -o /tmp/NotoSans.zip "*/hinted/ttf/NotoSans-$*.ttf" -d .
	rm /tmp/NotoSans.zip

# CJK fonts (subset OTFs from noto-cjk repo)
$(foreach s,$(CJK_STYLES),NotoSerifJP-$(s).otf): NotoSerifJP-%.otf:
	curl -sL $(GITHUB)/noto-cjk/releases/download/$(NOTO_CJK_SERIF_VER)/12_NotoSerifJP.zip -o /tmp/NotoSerifJP.zip
	unzip -j -o /tmp/NotoSerifJP.zip "*/NotoSerifJP-$*.otf" -d .
	rm /tmp/NotoSerifJP.zip

$(foreach s,$(CJK_STYLES),NotoSerifSC-$(s).otf): NotoSerifSC-%.otf:
	curl -sL $(GITHUB)/noto-cjk/releases/download/$(NOTO_CJK_SERIF_VER)/14_NotoSerifSC.zip -o /tmp/NotoSerifSC.zip
	unzip -j -o /tmp/NotoSerifSC.zip "*/NotoSerifSC-$*.otf" -d .
	rm /tmp/NotoSerifSC.zip

$(foreach s,$(CJK_STYLES),NotoSerifKR-$(s).otf): NotoSerifKR-%.otf:
	curl -sL $(GITHUB)/noto-cjk/releases/download/$(NOTO_CJK_SERIF_VER)/13_NotoSerifKR.zip -o /tmp/NotoSerifKR.zip
	unzip -j -o /tmp/NotoSerifKR.zip "*/NotoSerifKR-$*.otf" -d .
	rm /tmp/NotoSerifKR.zip

# Non-CJK script fonts (full/ttf variants)
$(foreach s,$(SCRIPT_STYLES),NotoNaskhArabic-$(s).ttf): NotoNaskhArabic-%.ttf:
	curl -sL $(GITHUB)/arabic/releases/download/$(NOTO_ARABIC_VER)/$(NOTO_ARABIC_VER).zip -o /tmp/NotoNaskhArabic.zip
	unzip -j -o /tmp/NotoNaskhArabic.zip "*/full/ttf/NotoNaskhArabic-$*.ttf" -d .
	rm /tmp/NotoNaskhArabic.zip

$(foreach s,$(SCRIPT_STYLES),NotoSerifHebrew-$(s).ttf): NotoSerifHebrew-%.ttf:
	curl -sL $(GITHUB)/hebrew/releases/download/$(NOTO_HEBREW_VER)/$(NOTO_HEBREW_VER).zip -o /tmp/NotoSerifHebrew.zip
	unzip -j -o /tmp/NotoSerifHebrew.zip "*/full/ttf/NotoSerifHebrew-$*.ttf" -d .
	rm /tmp/NotoSerifHebrew.zip

$(foreach s,$(SCRIPT_STYLES),NotoSerifDevanagari-$(s).ttf): NotoSerifDevanagari-%.ttf:
	curl -sL $(GITHUB)/devanagari/releases/download/$(NOTO_DEVANAGARI_VER)/$(NOTO_DEVANAGARI_VER).zip -o /tmp/NotoSerifDevanagari.zip
	unzip -j -o /tmp/NotoSerifDevanagari.zip "*/full/ttf/NotoSerifDevanagari-$*.ttf" -d .
	rm /tmp/NotoSerifDevanagari.zip

$(foreach s,$(SCRIPT_STYLES),NotoSerifThai-$(s).ttf): NotoSerifThai-%.ttf:
	curl -sL $(GITHUB)/thai/releases/download/$(NOTO_THAI_VER)/$(NOTO_THAI_VER).zip -o /tmp/NotoSerifThai.zip
	unzip -j -o /tmp/NotoSerifThai.zip "*/full/ttf/NotoSerifThai-$*.ttf" -d .
	rm /tmp/NotoSerifThai.zip

$(foreach s,$(SCRIPT_STYLES),NotoSerifGeorgian-$(s).ttf): NotoSerifGeorgian-%.ttf:
	curl -sL $(GITHUB)/georgian/releases/download/$(NOTO_GEORGIAN_VER)/$(NOTO_GEORGIAN_VER).zip -o /tmp/NotoSerifGeorgian.zip
	unzip -j -o /tmp/NotoSerifGeorgian.zip "*/full/ttf/NotoSerifGeorgian-$*.ttf" -d .
	rm /tmp/NotoSerifGeorgian.zip

clean:
	rm -f $(NOTO_FONTS)

.PHONY: all clean
