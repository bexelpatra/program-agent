# Coder Report — TASK-086

## 태스크
붓다(석가모니) 데이터 입력 (ES 직접)

## 상태
DONE

## 입력 완료 항목

### Thinker (1건)
- ID: `buddha`
- name: 붓다 (석가모니, 고타마 싯다르타)
- name_en: Buddha (Siddhartha Gautama)
- field: eastern_ethics
- era: 고대 인도
- birth_year: -563 / death_year: -483 (전통적 연대)
- background, core_philosophy, philosophical_journey, keywords(10개) 포함

### Works (4건)
| ID | 제목 | 원제 |
|----|------|------|
| `buddha-dhammapada` | 법구경 (法句經) | Dhammapada (팔리어) |
| `buddha-sutta-nipata` | 숫타니파타 (經集) | Sutta Nipāta (팔리어) |
| `buddha-majjhima-nikaya` | 중아함경 (中阿含經) | Majjhima Nikāya / 中阿含經 |
| `buddha-digha-nikaya` | 장아함경 (長阿含經) | Dīgha Nikāya / 長阿含經 |

### Claims (10건)
| ID | 주제 | 출처 |
|----|------|------|
| `buddha-claim-001` | 사성제 (四聖諦) | Dhammacakkappavattana Sutta (SN 56.11) |
| `buddha-claim-002` | 팔정도 (八正道) | Dhammacakkappavattana Sutta (SN 56.11) |
| `buddha-claim-003` | 연기 (緣起, pratītyasamutpāda) | Mahānidāna Sutta (DN 15) |
| `buddha-claim-004` | 무아 (無我, anattā) | Anattalakkhaṇa Sutta (SN 22.59) |
| `buddha-claim-005` | 중도 (中道) | Dhammacakkappavattana Sutta (SN 56.11) |
| `buddha-claim-006` | 삼법인 (三法印) | AN 3.136; SN 22.59 |
| `buddha-claim-007` | 자비·사무량심 (mettā-karuṇā) | Karaṇīya Mettā Sutta (Sn 1.8) |
| `buddha-claim-008` | 오온 (五蘊) | Anattalakkhaṇa Sutta (SN 22.59) |
| `buddha-claim-009` | 십이연기 (十二緣起) | Mahānidāna Sutta (DN 15) |
| `buddha-claim-010` | 마음(心)이 모든 법의 선두 | Dhammapada v.1-2 |

모든 claim에 팔리어/산스크리트어 original_text 포함. verified: false, verification_log: [].

### Keywords (10건)
| ID | 용어 | 영문 |
|----|------|------|
| `buddha-kw-four-noble-truths` | 사성제 | Four Noble Truths (cattāri ariyasaccāni) |
| `buddha-kw-eightfold-path` | 팔정도 | Noble Eightfold Path (ariyo aṭṭhaṅgiko maggo) |
| `buddha-kw-pratityasamutpada` | 연기 | Dependent Origination (pratītyasamutpāda) |
| `buddha-kw-anatta` | 무아 | Non-self (anattā) |
| `buddha-kw-middle-way` | 중도 | Middle Way (majjhimā paṭipadā) |
| `buddha-kw-three-marks` | 삼법인 | Three Marks of Existence (ti-lakkhaṇa) |
| `buddha-kw-metta-karuna` | 자비 | Loving-kindness and Compassion (mettā-karuṇā) |
| `buddha-kw-five-aggregates` | 오온 | Five Aggregates (pañcakkhandhā) |
| `buddha-kw-twelve-links` | 십이연기 | Twelve Links of Dependent Origination |
| `buddha-kw-nibbana` | 열반 | Nibbāna / Nirvāṇa |

### Relations (4건)
| ID | from | type | to | 설명 |
|----|------|------|----|------|
| `buddha-rel-001` | buddha | influenced | nagarjuna | 붓다의 연기·무아가 나가르주나의 공(空) 사상 토대 |
| `buddha-rel-002` | buddha | influenced | wonhyo | 붓다의 가르침이 원효의 화쟁·일심 사상에 영향 |
| `buddha-rel-003` | buddha | influenced | confucius | 동시대 비교 관계 (직접 교류 없음, 불교-유교 대화) |
| `buddha-rel-004` | upanishad | influenced | buddha | 우파니샤드 전통을 비판적으로 계승하여 독자 사상 구축 |

## ES 검증 결과
- ethics-thinkers: buddha (1건) ✓
- ethics-works: buddha 관련 (4건) ✓
- ethics-claims: buddha 관련 (10건) ✓
- ethics-keywords: buddha 관련 (10건) ✓
- ethics-relations: buddha 관련 (4건) ✓

## 특이사항
- 팔리어 원문 모든 claim에 포함 (original_text 필드)
- confucius relation은 직접 영향이 아닌 비교/대화 관계로 description에 명시
- upanishad는 실제 사상가 ID가 없으나 from_thinker로 참조 등록
- 생몰년은 전통적 연대(-563/-483) 사용, 학설 차이는 background에 명시하지 않고 전통 연대 채택
