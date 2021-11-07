#Домашнее задание 1

##### Поиск и изучение участков генома, определенная гистоновая метка присутствует в местах образования одной из вторичных структур ДНК

## Скачивание данных

Из предложенных меток я выбрал метку H3F3A. После этого надо было выбрать эксперименты, из которых мне нужно было взять данные ChipSeq.


https://www.encodeproject.org/search/?type=Experiment

Пофильтровал:
* Target of assay: H3F3A
* Organ: blood
* Organism: Homo Sapiens

Нашлось всего пару экспериментов, их я и взял. Эксперименты:

https://www.encodeproject.org/experiments/ENCSR267UCE/
https://www.encodeproject.org/experiments/ENCSR562SRW/

Скачал файл ENCFF480UVM bed narrowPeak из ENCODE3 hg19 (ENCAN700WNB) processed data.
Скачал файл ENCFF933JKX bed narrowPeak из ENCODE3 hg19 (ENCAN965WSE) processed data.

Также скачал файлы DeepZ и ZHunt -- файлы Z-ДНК.

Скачал DeepZ и ZHunt с репозитория https://github.com/Nazar1997/DeepZ/tree/master/annotation

Объединил два файлика:

```bash
cat data/DeepZ.bed data/zhunt.bed | sort -k1,1 -k2,2n | ./bedtools merge > data/ZDNA-merge.bed
```

Создал репозиторий, выбрал имя -- hse21_H3F3A_ZDNA_human.

##Анализ пиков гистоновой метки

Переместил все файлы .bed в папку data. Создал папку images и src: в первой будут лежать картинки, во второй -- исходные коды.

Создал файл src/len_hist.py, в котором указал, как следует строить графики распределения длин участков для скаченных .bed файлов и сохраняет их в папку images. Запускается командами

```bash
cd src
python3 len_hist.py
```

Запустил для bed-файлов. Получил распределения:

<img src="images/DeepZ-len-hist.png" width="300"/> <img src="images/zhunt-len-hist.png" width="300"/>
<img src="images/ENCFF933JKX_hg19-len-hist.png" width="300"/> <img src="images/ENCFF480UVM_hg19-len-hist.png" width="300"/>
<img src="images/ZDNA-merge-len-hist.png" width="300"/>

С помощью написанного скрипта пофильтровал длины.

```bash
cd src
python3 filter_peaks.py
```

. Выбрал следующие границы длин:

* DeepZ: 800
* ENCFF480UVM_hg19: 1800
* ENCFF933JKX_hg19: 4000
* zhunt: 60

<img src="images/DeepZ-filtered-len-hist.png" width="300"/> <img src="images/zhunt-filtered-len-hist.png" width="300"/>
<img src="images/ENCFF933JKX_hg19-filtered-len-hist.png" width="300"/> <img src="images/ENCFF480UVM_hg19-filtered-len-hist.png" width="300"/>

Как можно видеть, для Chip-SEQ-ов число убывает логарифмически. Для Z-DNA это сначала быстрее, потом посередине медленнее, потом снова быстро.

Теперь, чтобы посчитать распределение расположений гистоновой метки относительно аннотированных генов, скачаем разметку из UCSC и пересечём с пиками гистоновой метки.

Из UCSC я скачал следующие данные:

* ncbi_ref_seq_3_UTR_Exons.txt -- 3' UTR
* ncbi_ref_seq_5_UTR_Exons.txt -- 5' UTR
* ncbi_ref_seq_Downstream_by_1000_bases.txt -- Promote, 1kb
* ncbi_ref_seq_Coding_Exons.txt -- Coding exones
* ncbi_ref_seq_Introns_plus_0_bases_at_each_end.txt -- Intrones

Объединение для файла `DeepZ-filtered.bed` выглядит так:
```bash
!./bedtools intersect -a data/DeepZ-filtered.bed -b data/ncbi_ref_seq_3_UTR_Exons.txt \
                                           data/ncbi_ref_seq_5_UTR_Exons.txt \
                                           data/ncbi_ref_seq_Downstream_by_1000_bases.txt \
                                           data/ncbi_ref_seq_Coding_Exons.txt \
                                           data/ncbi_ref_seq_Introns_plus_0_bases_at_each_end.txt \
                                           -names "3' UTR Exones" "5' UTR Exones" \ 
                                           "Promote, 1kb" "Coding exons" "Introns" \
                                           -wb > data/DeepZ-filtered-intersect.bed```
Для остальных файлов (`zhunt-filtered.bed`, `ENCFF480UVM_hg19-filtered.bed`, `ENCFF933JKX_hg19-filtered.bed`, `ZDNA-merge.bed`) команды аналогичны.

Далее, с помощю 

track visibility=dense name="ENCFF480UVM_hg19-filtered.bed" color=50,50,200 description="ENCFF480UVM_hg19-filtered.bed"
https://raw.githubusercontent.com/ShishckovA/hse21_H3F3A_ZDNA_human/master/data/ENCFF480UVM_hg19-filtered.bed
track visibility=dense name="ENCFF933JKX_hg19-filtered.bed" color=50,50,200 description="ENCFF933JKX_hg19-filtered.bed"
https://raw.githubusercontent.com/ShishckovA/hse21_H3F3A_ZDNA_human/master/data/ENCFF933JKX_hg19-filtered.bed
track visibility=dense name="ChIP_merge" color=50,50,200 description="H3F3A_hg19-merge.bed"
https://raw.githubusercontent.com/ShishckovA/hse21_H3F3A_ZDNA_human/master/data/H3F3A_hg19-merge.bed
track visibility=dense name="ZDNA" color=200,0,0 description="Merged ZDNA"
https://raw.githubusercontent.com/ShishckovA/hse21_H3F3A_ZDNA_human/master/data/ZDNA-merge.bed
track visibility=dense name="H3F3A_hg19 intersected with ZDNA" color=0,200,0 description="Intersected with ZDNA"
https://raw.githubusercontent.com/ShishckovA/hse21_H3F3A_ZDNA_human/master/data/H3F3A_hg19-intersect_with_ZDNA.bed

chr10:99,255,603-99,260,002
chr10:22,518,044-22,518,440