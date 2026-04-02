# yoneda-in-tongues

State the [Yoneda lemma](https://ncatlab.org/nlab/show/Yoneda+lemma) in every language.

Contribute, acknowledge yourself, sign your translation (and provide, if you want, a proof of your knowledge of the language you write in!).

## Contributing

Check [INDEX.md](INDEX.md) for the full list of languages, types, and contributors.

Add a file `src/<code>.tex` with a `% contributors:` comment and a `\tran` call:

```latex
% contributors: @your-github-handle
\tran{Language Name (ISO 639-3 xxx)}{Lemma Name}{
	Translation text with $\hom(-,X)\Rightarrow F$ math...
	\[
		\Big(\xi : \hom(-,X)\Rightarrow F\Big) \mapsto \xi_X(1_X)
	\]
	(closing remark).
}
```

Then add `\input{src/xxx}` to `YIT.tex` under the appropriate language family section.

The `% contributors:` line is a comma-separated list of GitHub handles in chronological order. Append yours when you contribute.

### Reviewing translations

All translations benefit from review. If you speak a language that's already listed, improving the phrasing, fixing grammar, or correcting a technical term is a valuable contribution — just add your handle to the `% contributors:` line.

Many translations were machine-generated and have an empty `% contributors:` field. These especially need a native speaker's eye.

### Naming conventions

* [**ISO 639-3**](https://iso639-3.sil.org/code_tables/639/data) codes for the filename (e.g. `src/fra.tex`, `src/jpn.tex`)
* [**CLCR**](https://www.kreativekorp.com/clcr/) long-form codes for fictional languages without ISO 639-3 (e.g. `src/art-x-dothraki.tex`)
* **Folder per language** when multiple scripts exist (e.g. `src/tok/latin.tex`, `src/tok/sitelen.tex`)

### Translation guidelines

* The English translation (`src/eng.tex`) is the base — preserve its structure
* Keep it simple; avoid subordination when possible
* It's all about learning technical words (what is the right translation for "functor" in Quenya?)
* Provide references for technical terms; propose, propose, propose
* Unusual languages are more than welcome (Ithkuil, anybody?)
* Cooperate. Discuss. Re-read what is already written

## Building

The project uses XeLaTeX. With [Nix](https://nixos.org/):

```sh
nix develop    # enter devShell with texlive scheme-full
make           # build YIT.pdf
```

The main font is [Quivira](http://www.quivira-font.com/) (`fonts/Quivira.otf`), covering a large slice of the Unicode character map. Additional system fonts are used for CJK, RTL, Indic, Thai, and Georgian scripts — see the preamble of `YIT.tex` for the full list.
