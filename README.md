## Reqs
```
pip install flask
pip install python-dotenv
pip install -U spacy
pip install wheel
```
follow `https://github.com/danielibanezgarcia/less`
    `https://freeling-user-manual.readthedocs.io/en/v4.2/installation/requirements-mac/`
    `https://github.com/AdoptOpenJDK/homebrew-openjdk`
        `brew install --cask temurin8`
    `pip install JPype1 jvm`
    `pip install uralicNLP` <– important; I modified the less code to use this

have to edit:
    change `config.py` path to `/Library/Java/JavaVirtualMachines/temurin-11.jdk/Contents/Home/lib/server/libjvm.dylib` or similar

circumventing current weirdness:
   - version of pyYAML project uses doesn't support cpython3.0 so you have to `pip install "cython<3.0.0" && pip install --no-build-isolation pyyaml==5.4.1`
   - 


https://github.com/danielibanezgarcia/less



## Citation

Deleted:
Todo `https://github.com/qiang2100/BERT-LS`(but quite edited and using the pretrained ES from the following:)
    `https://github.com/LaSTUS-TALN-UPF/TSAR-LSBert` : `https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.es.300.vec.gz`