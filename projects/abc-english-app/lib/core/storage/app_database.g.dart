// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_database.dart';

// ignore_for_file: type=lint
class $EpisodesTable extends Episodes
    with TableInfo<$EpisodesTable, EpisodeRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $EpisodesTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _idMeta = const VerificationMeta('id');
  @override
  late final GeneratedColumn<String> id = GeneratedColumn<String>(
    'id',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _titleMeta = const VerificationMeta('title');
  @override
  late final GeneratedColumn<String> title = GeneratedColumn<String>(
    'title',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _publishedDateMeta = const VerificationMeta(
    'publishedDate',
  );
  @override
  late final GeneratedColumn<DateTime> publishedDate =
      GeneratedColumn<DateTime>(
        'published_date',
        aliasedName,
        false,
        type: DriftSqlType.dateTime,
        requiredDuringInsert: true,
      );
  static const VerificationMeta _durationMsMeta = const VerificationMeta(
    'durationMs',
  );
  @override
  late final GeneratedColumn<int> durationMs = GeneratedColumn<int>(
    'duration_ms',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _avgWerMeta = const VerificationMeta('avgWer');
  @override
  late final GeneratedColumn<double> avgWer = GeneratedColumn<double>(
    'avg_wer',
    aliasedName,
    true,
    type: DriftSqlType.double,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _lastModifiedMeta = const VerificationMeta(
    'lastModified',
  );
  @override
  late final GeneratedColumn<DateTime> lastModified = GeneratedColumn<DateTime>(
    'last_modified',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _downloadedAtMeta = const VerificationMeta(
    'downloadedAt',
  );
  @override
  late final GeneratedColumn<DateTime> downloadedAt = GeneratedColumn<DateTime>(
    'downloaded_at',
    aliasedName,
    true,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _audioLocalPathMeta = const VerificationMeta(
    'audioLocalPath',
  );
  @override
  late final GeneratedColumn<String> audioLocalPath = GeneratedColumn<String>(
    'audio_local_path',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  @override
  List<GeneratedColumn> get $columns => [
    id,
    title,
    publishedDate,
    durationMs,
    avgWer,
    lastModified,
    downloadedAt,
    audioLocalPath,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'episodes';
  @override
  VerificationContext validateIntegrity(
    Insertable<EpisodeRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('id')) {
      context.handle(_idMeta, id.isAcceptableOrUnknown(data['id']!, _idMeta));
    } else if (isInserting) {
      context.missing(_idMeta);
    }
    if (data.containsKey('title')) {
      context.handle(
        _titleMeta,
        title.isAcceptableOrUnknown(data['title']!, _titleMeta),
      );
    } else if (isInserting) {
      context.missing(_titleMeta);
    }
    if (data.containsKey('published_date')) {
      context.handle(
        _publishedDateMeta,
        publishedDate.isAcceptableOrUnknown(
          data['published_date']!,
          _publishedDateMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_publishedDateMeta);
    }
    if (data.containsKey('duration_ms')) {
      context.handle(
        _durationMsMeta,
        durationMs.isAcceptableOrUnknown(data['duration_ms']!, _durationMsMeta),
      );
    } else if (isInserting) {
      context.missing(_durationMsMeta);
    }
    if (data.containsKey('avg_wer')) {
      context.handle(
        _avgWerMeta,
        avgWer.isAcceptableOrUnknown(data['avg_wer']!, _avgWerMeta),
      );
    }
    if (data.containsKey('last_modified')) {
      context.handle(
        _lastModifiedMeta,
        lastModified.isAcceptableOrUnknown(
          data['last_modified']!,
          _lastModifiedMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_lastModifiedMeta);
    }
    if (data.containsKey('downloaded_at')) {
      context.handle(
        _downloadedAtMeta,
        downloadedAt.isAcceptableOrUnknown(
          data['downloaded_at']!,
          _downloadedAtMeta,
        ),
      );
    }
    if (data.containsKey('audio_local_path')) {
      context.handle(
        _audioLocalPathMeta,
        audioLocalPath.isAcceptableOrUnknown(
          data['audio_local_path']!,
          _audioLocalPathMeta,
        ),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {id};
  @override
  EpisodeRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return EpisodeRow(
      id: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}id'],
      )!,
      title: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}title'],
      )!,
      publishedDate: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}published_date'],
      )!,
      durationMs: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}duration_ms'],
      )!,
      avgWer: attachedDatabase.typeMapping.read(
        DriftSqlType.double,
        data['${effectivePrefix}avg_wer'],
      ),
      lastModified: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}last_modified'],
      )!,
      downloadedAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}downloaded_at'],
      ),
      audioLocalPath: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}audio_local_path'],
      ),
    );
  }

  @override
  $EpisodesTable createAlias(String alias) {
    return $EpisodesTable(attachedDatabase, alias);
  }
}

class EpisodeRow extends DataClass implements Insertable<EpisodeRow> {
  final String id;
  final String title;
  final DateTime publishedDate;
  final int durationMs;
  final double? avgWer;
  final DateTime lastModified;
  final DateTime? downloadedAt;
  final String? audioLocalPath;
  const EpisodeRow({
    required this.id,
    required this.title,
    required this.publishedDate,
    required this.durationMs,
    this.avgWer,
    required this.lastModified,
    this.downloadedAt,
    this.audioLocalPath,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['id'] = Variable<String>(id);
    map['title'] = Variable<String>(title);
    map['published_date'] = Variable<DateTime>(publishedDate);
    map['duration_ms'] = Variable<int>(durationMs);
    if (!nullToAbsent || avgWer != null) {
      map['avg_wer'] = Variable<double>(avgWer);
    }
    map['last_modified'] = Variable<DateTime>(lastModified);
    if (!nullToAbsent || downloadedAt != null) {
      map['downloaded_at'] = Variable<DateTime>(downloadedAt);
    }
    if (!nullToAbsent || audioLocalPath != null) {
      map['audio_local_path'] = Variable<String>(audioLocalPath);
    }
    return map;
  }

  EpisodesCompanion toCompanion(bool nullToAbsent) {
    return EpisodesCompanion(
      id: Value(id),
      title: Value(title),
      publishedDate: Value(publishedDate),
      durationMs: Value(durationMs),
      avgWer: avgWer == null && nullToAbsent
          ? const Value.absent()
          : Value(avgWer),
      lastModified: Value(lastModified),
      downloadedAt: downloadedAt == null && nullToAbsent
          ? const Value.absent()
          : Value(downloadedAt),
      audioLocalPath: audioLocalPath == null && nullToAbsent
          ? const Value.absent()
          : Value(audioLocalPath),
    );
  }

  factory EpisodeRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return EpisodeRow(
      id: serializer.fromJson<String>(json['id']),
      title: serializer.fromJson<String>(json['title']),
      publishedDate: serializer.fromJson<DateTime>(json['publishedDate']),
      durationMs: serializer.fromJson<int>(json['durationMs']),
      avgWer: serializer.fromJson<double?>(json['avgWer']),
      lastModified: serializer.fromJson<DateTime>(json['lastModified']),
      downloadedAt: serializer.fromJson<DateTime?>(json['downloadedAt']),
      audioLocalPath: serializer.fromJson<String?>(json['audioLocalPath']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'id': serializer.toJson<String>(id),
      'title': serializer.toJson<String>(title),
      'publishedDate': serializer.toJson<DateTime>(publishedDate),
      'durationMs': serializer.toJson<int>(durationMs),
      'avgWer': serializer.toJson<double?>(avgWer),
      'lastModified': serializer.toJson<DateTime>(lastModified),
      'downloadedAt': serializer.toJson<DateTime?>(downloadedAt),
      'audioLocalPath': serializer.toJson<String?>(audioLocalPath),
    };
  }

  EpisodeRow copyWith({
    String? id,
    String? title,
    DateTime? publishedDate,
    int? durationMs,
    Value<double?> avgWer = const Value.absent(),
    DateTime? lastModified,
    Value<DateTime?> downloadedAt = const Value.absent(),
    Value<String?> audioLocalPath = const Value.absent(),
  }) => EpisodeRow(
    id: id ?? this.id,
    title: title ?? this.title,
    publishedDate: publishedDate ?? this.publishedDate,
    durationMs: durationMs ?? this.durationMs,
    avgWer: avgWer.present ? avgWer.value : this.avgWer,
    lastModified: lastModified ?? this.lastModified,
    downloadedAt: downloadedAt.present ? downloadedAt.value : this.downloadedAt,
    audioLocalPath: audioLocalPath.present
        ? audioLocalPath.value
        : this.audioLocalPath,
  );
  EpisodeRow copyWithCompanion(EpisodesCompanion data) {
    return EpisodeRow(
      id: data.id.present ? data.id.value : this.id,
      title: data.title.present ? data.title.value : this.title,
      publishedDate: data.publishedDate.present
          ? data.publishedDate.value
          : this.publishedDate,
      durationMs: data.durationMs.present
          ? data.durationMs.value
          : this.durationMs,
      avgWer: data.avgWer.present ? data.avgWer.value : this.avgWer,
      lastModified: data.lastModified.present
          ? data.lastModified.value
          : this.lastModified,
      downloadedAt: data.downloadedAt.present
          ? data.downloadedAt.value
          : this.downloadedAt,
      audioLocalPath: data.audioLocalPath.present
          ? data.audioLocalPath.value
          : this.audioLocalPath,
    );
  }

  @override
  String toString() {
    return (StringBuffer('EpisodeRow(')
          ..write('id: $id, ')
          ..write('title: $title, ')
          ..write('publishedDate: $publishedDate, ')
          ..write('durationMs: $durationMs, ')
          ..write('avgWer: $avgWer, ')
          ..write('lastModified: $lastModified, ')
          ..write('downloadedAt: $downloadedAt, ')
          ..write('audioLocalPath: $audioLocalPath')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(
    id,
    title,
    publishedDate,
    durationMs,
    avgWer,
    lastModified,
    downloadedAt,
    audioLocalPath,
  );
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is EpisodeRow &&
          other.id == this.id &&
          other.title == this.title &&
          other.publishedDate == this.publishedDate &&
          other.durationMs == this.durationMs &&
          other.avgWer == this.avgWer &&
          other.lastModified == this.lastModified &&
          other.downloadedAt == this.downloadedAt &&
          other.audioLocalPath == this.audioLocalPath);
}

class EpisodesCompanion extends UpdateCompanion<EpisodeRow> {
  final Value<String> id;
  final Value<String> title;
  final Value<DateTime> publishedDate;
  final Value<int> durationMs;
  final Value<double?> avgWer;
  final Value<DateTime> lastModified;
  final Value<DateTime?> downloadedAt;
  final Value<String?> audioLocalPath;
  final Value<int> rowid;
  const EpisodesCompanion({
    this.id = const Value.absent(),
    this.title = const Value.absent(),
    this.publishedDate = const Value.absent(),
    this.durationMs = const Value.absent(),
    this.avgWer = const Value.absent(),
    this.lastModified = const Value.absent(),
    this.downloadedAt = const Value.absent(),
    this.audioLocalPath = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  EpisodesCompanion.insert({
    required String id,
    required String title,
    required DateTime publishedDate,
    required int durationMs,
    this.avgWer = const Value.absent(),
    required DateTime lastModified,
    this.downloadedAt = const Value.absent(),
    this.audioLocalPath = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : id = Value(id),
       title = Value(title),
       publishedDate = Value(publishedDate),
       durationMs = Value(durationMs),
       lastModified = Value(lastModified);
  static Insertable<EpisodeRow> custom({
    Expression<String>? id,
    Expression<String>? title,
    Expression<DateTime>? publishedDate,
    Expression<int>? durationMs,
    Expression<double>? avgWer,
    Expression<DateTime>? lastModified,
    Expression<DateTime>? downloadedAt,
    Expression<String>? audioLocalPath,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (id != null) 'id': id,
      if (title != null) 'title': title,
      if (publishedDate != null) 'published_date': publishedDate,
      if (durationMs != null) 'duration_ms': durationMs,
      if (avgWer != null) 'avg_wer': avgWer,
      if (lastModified != null) 'last_modified': lastModified,
      if (downloadedAt != null) 'downloaded_at': downloadedAt,
      if (audioLocalPath != null) 'audio_local_path': audioLocalPath,
      if (rowid != null) 'rowid': rowid,
    });
  }

  EpisodesCompanion copyWith({
    Value<String>? id,
    Value<String>? title,
    Value<DateTime>? publishedDate,
    Value<int>? durationMs,
    Value<double?>? avgWer,
    Value<DateTime>? lastModified,
    Value<DateTime?>? downloadedAt,
    Value<String?>? audioLocalPath,
    Value<int>? rowid,
  }) {
    return EpisodesCompanion(
      id: id ?? this.id,
      title: title ?? this.title,
      publishedDate: publishedDate ?? this.publishedDate,
      durationMs: durationMs ?? this.durationMs,
      avgWer: avgWer ?? this.avgWer,
      lastModified: lastModified ?? this.lastModified,
      downloadedAt: downloadedAt ?? this.downloadedAt,
      audioLocalPath: audioLocalPath ?? this.audioLocalPath,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (id.present) {
      map['id'] = Variable<String>(id.value);
    }
    if (title.present) {
      map['title'] = Variable<String>(title.value);
    }
    if (publishedDate.present) {
      map['published_date'] = Variable<DateTime>(publishedDate.value);
    }
    if (durationMs.present) {
      map['duration_ms'] = Variable<int>(durationMs.value);
    }
    if (avgWer.present) {
      map['avg_wer'] = Variable<double>(avgWer.value);
    }
    if (lastModified.present) {
      map['last_modified'] = Variable<DateTime>(lastModified.value);
    }
    if (downloadedAt.present) {
      map['downloaded_at'] = Variable<DateTime>(downloadedAt.value);
    }
    if (audioLocalPath.present) {
      map['audio_local_path'] = Variable<String>(audioLocalPath.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('EpisodesCompanion(')
          ..write('id: $id, ')
          ..write('title: $title, ')
          ..write('publishedDate: $publishedDate, ')
          ..write('durationMs: $durationMs, ')
          ..write('avgWer: $avgWer, ')
          ..write('lastModified: $lastModified, ')
          ..write('downloadedAt: $downloadedAt, ')
          ..write('audioLocalPath: $audioLocalPath, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

class $SentencesTable extends Sentences
    with TableInfo<$SentencesTable, SentenceRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $SentencesTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _episodeIdMeta = const VerificationMeta(
    'episodeId',
  );
  @override
  late final GeneratedColumn<String> episodeId = GeneratedColumn<String>(
    'episode_id',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
    defaultConstraints: GeneratedColumn.constraintIsAlways(
      'REFERENCES episodes (id)',
    ),
  );
  static const VerificationMeta _sentenceIndexMeta = const VerificationMeta(
    'sentenceIndex',
  );
  @override
  late final GeneratedColumn<int> sentenceIndex = GeneratedColumn<int>(
    'index',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _bodyMeta = const VerificationMeta('body');
  @override
  late final GeneratedColumn<String> body = GeneratedColumn<String>(
    'text',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _startMsMeta = const VerificationMeta(
    'startMs',
  );
  @override
  late final GeneratedColumn<int> startMs = GeneratedColumn<int>(
    'start_ms',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _endMsMeta = const VerificationMeta('endMs');
  @override
  late final GeneratedColumn<int> endMs = GeneratedColumn<int>(
    'end_ms',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _werMeta = const VerificationMeta('wer');
  @override
  late final GeneratedColumn<double> wer = GeneratedColumn<double>(
    'wer',
    aliasedName,
    true,
    type: DriftSqlType.double,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _difficultyMeta = const VerificationMeta(
    'difficulty',
  );
  @override
  late final GeneratedColumn<String> difficulty = GeneratedColumn<String>(
    'difficulty',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  @override
  List<GeneratedColumn> get $columns => [
    episodeId,
    sentenceIndex,
    body,
    startMs,
    endMs,
    wer,
    difficulty,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'sentences';
  @override
  VerificationContext validateIntegrity(
    Insertable<SentenceRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('episode_id')) {
      context.handle(
        _episodeIdMeta,
        episodeId.isAcceptableOrUnknown(data['episode_id']!, _episodeIdMeta),
      );
    } else if (isInserting) {
      context.missing(_episodeIdMeta);
    }
    if (data.containsKey('index')) {
      context.handle(
        _sentenceIndexMeta,
        sentenceIndex.isAcceptableOrUnknown(data['index']!, _sentenceIndexMeta),
      );
    } else if (isInserting) {
      context.missing(_sentenceIndexMeta);
    }
    if (data.containsKey('text')) {
      context.handle(
        _bodyMeta,
        body.isAcceptableOrUnknown(data['text']!, _bodyMeta),
      );
    } else if (isInserting) {
      context.missing(_bodyMeta);
    }
    if (data.containsKey('start_ms')) {
      context.handle(
        _startMsMeta,
        startMs.isAcceptableOrUnknown(data['start_ms']!, _startMsMeta),
      );
    } else if (isInserting) {
      context.missing(_startMsMeta);
    }
    if (data.containsKey('end_ms')) {
      context.handle(
        _endMsMeta,
        endMs.isAcceptableOrUnknown(data['end_ms']!, _endMsMeta),
      );
    } else if (isInserting) {
      context.missing(_endMsMeta);
    }
    if (data.containsKey('wer')) {
      context.handle(
        _werMeta,
        wer.isAcceptableOrUnknown(data['wer']!, _werMeta),
      );
    }
    if (data.containsKey('difficulty')) {
      context.handle(
        _difficultyMeta,
        difficulty.isAcceptableOrUnknown(data['difficulty']!, _difficultyMeta),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {episodeId, sentenceIndex};
  @override
  SentenceRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return SentenceRow(
      episodeId: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}episode_id'],
      )!,
      sentenceIndex: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}index'],
      )!,
      body: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}text'],
      )!,
      startMs: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}start_ms'],
      )!,
      endMs: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}end_ms'],
      )!,
      wer: attachedDatabase.typeMapping.read(
        DriftSqlType.double,
        data['${effectivePrefix}wer'],
      ),
      difficulty: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}difficulty'],
      ),
    );
  }

  @override
  $SentencesTable createAlias(String alias) {
    return $SentencesTable(attachedDatabase, alias);
  }
}

class SentenceRow extends DataClass implements Insertable<SentenceRow> {
  final String episodeId;
  final int sentenceIndex;
  final String body;
  final int startMs;
  final int endMs;
  final double? wer;
  final String? difficulty;
  const SentenceRow({
    required this.episodeId,
    required this.sentenceIndex,
    required this.body,
    required this.startMs,
    required this.endMs,
    this.wer,
    this.difficulty,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['episode_id'] = Variable<String>(episodeId);
    map['index'] = Variable<int>(sentenceIndex);
    map['text'] = Variable<String>(body);
    map['start_ms'] = Variable<int>(startMs);
    map['end_ms'] = Variable<int>(endMs);
    if (!nullToAbsent || wer != null) {
      map['wer'] = Variable<double>(wer);
    }
    if (!nullToAbsent || difficulty != null) {
      map['difficulty'] = Variable<String>(difficulty);
    }
    return map;
  }

  SentencesCompanion toCompanion(bool nullToAbsent) {
    return SentencesCompanion(
      episodeId: Value(episodeId),
      sentenceIndex: Value(sentenceIndex),
      body: Value(body),
      startMs: Value(startMs),
      endMs: Value(endMs),
      wer: wer == null && nullToAbsent ? const Value.absent() : Value(wer),
      difficulty: difficulty == null && nullToAbsent
          ? const Value.absent()
          : Value(difficulty),
    );
  }

  factory SentenceRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return SentenceRow(
      episodeId: serializer.fromJson<String>(json['episodeId']),
      sentenceIndex: serializer.fromJson<int>(json['sentenceIndex']),
      body: serializer.fromJson<String>(json['body']),
      startMs: serializer.fromJson<int>(json['startMs']),
      endMs: serializer.fromJson<int>(json['endMs']),
      wer: serializer.fromJson<double?>(json['wer']),
      difficulty: serializer.fromJson<String?>(json['difficulty']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'episodeId': serializer.toJson<String>(episodeId),
      'sentenceIndex': serializer.toJson<int>(sentenceIndex),
      'body': serializer.toJson<String>(body),
      'startMs': serializer.toJson<int>(startMs),
      'endMs': serializer.toJson<int>(endMs),
      'wer': serializer.toJson<double?>(wer),
      'difficulty': serializer.toJson<String?>(difficulty),
    };
  }

  SentenceRow copyWith({
    String? episodeId,
    int? sentenceIndex,
    String? body,
    int? startMs,
    int? endMs,
    Value<double?> wer = const Value.absent(),
    Value<String?> difficulty = const Value.absent(),
  }) => SentenceRow(
    episodeId: episodeId ?? this.episodeId,
    sentenceIndex: sentenceIndex ?? this.sentenceIndex,
    body: body ?? this.body,
    startMs: startMs ?? this.startMs,
    endMs: endMs ?? this.endMs,
    wer: wer.present ? wer.value : this.wer,
    difficulty: difficulty.present ? difficulty.value : this.difficulty,
  );
  SentenceRow copyWithCompanion(SentencesCompanion data) {
    return SentenceRow(
      episodeId: data.episodeId.present ? data.episodeId.value : this.episodeId,
      sentenceIndex: data.sentenceIndex.present
          ? data.sentenceIndex.value
          : this.sentenceIndex,
      body: data.body.present ? data.body.value : this.body,
      startMs: data.startMs.present ? data.startMs.value : this.startMs,
      endMs: data.endMs.present ? data.endMs.value : this.endMs,
      wer: data.wer.present ? data.wer.value : this.wer,
      difficulty: data.difficulty.present
          ? data.difficulty.value
          : this.difficulty,
    );
  }

  @override
  String toString() {
    return (StringBuffer('SentenceRow(')
          ..write('episodeId: $episodeId, ')
          ..write('sentenceIndex: $sentenceIndex, ')
          ..write('body: $body, ')
          ..write('startMs: $startMs, ')
          ..write('endMs: $endMs, ')
          ..write('wer: $wer, ')
          ..write('difficulty: $difficulty')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(
    episodeId,
    sentenceIndex,
    body,
    startMs,
    endMs,
    wer,
    difficulty,
  );
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is SentenceRow &&
          other.episodeId == this.episodeId &&
          other.sentenceIndex == this.sentenceIndex &&
          other.body == this.body &&
          other.startMs == this.startMs &&
          other.endMs == this.endMs &&
          other.wer == this.wer &&
          other.difficulty == this.difficulty);
}

class SentencesCompanion extends UpdateCompanion<SentenceRow> {
  final Value<String> episodeId;
  final Value<int> sentenceIndex;
  final Value<String> body;
  final Value<int> startMs;
  final Value<int> endMs;
  final Value<double?> wer;
  final Value<String?> difficulty;
  final Value<int> rowid;
  const SentencesCompanion({
    this.episodeId = const Value.absent(),
    this.sentenceIndex = const Value.absent(),
    this.body = const Value.absent(),
    this.startMs = const Value.absent(),
    this.endMs = const Value.absent(),
    this.wer = const Value.absent(),
    this.difficulty = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  SentencesCompanion.insert({
    required String episodeId,
    required int sentenceIndex,
    required String body,
    required int startMs,
    required int endMs,
    this.wer = const Value.absent(),
    this.difficulty = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : episodeId = Value(episodeId),
       sentenceIndex = Value(sentenceIndex),
       body = Value(body),
       startMs = Value(startMs),
       endMs = Value(endMs);
  static Insertable<SentenceRow> custom({
    Expression<String>? episodeId,
    Expression<int>? sentenceIndex,
    Expression<String>? body,
    Expression<int>? startMs,
    Expression<int>? endMs,
    Expression<double>? wer,
    Expression<String>? difficulty,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (episodeId != null) 'episode_id': episodeId,
      if (sentenceIndex != null) 'index': sentenceIndex,
      if (body != null) 'text': body,
      if (startMs != null) 'start_ms': startMs,
      if (endMs != null) 'end_ms': endMs,
      if (wer != null) 'wer': wer,
      if (difficulty != null) 'difficulty': difficulty,
      if (rowid != null) 'rowid': rowid,
    });
  }

  SentencesCompanion copyWith({
    Value<String>? episodeId,
    Value<int>? sentenceIndex,
    Value<String>? body,
    Value<int>? startMs,
    Value<int>? endMs,
    Value<double?>? wer,
    Value<String?>? difficulty,
    Value<int>? rowid,
  }) {
    return SentencesCompanion(
      episodeId: episodeId ?? this.episodeId,
      sentenceIndex: sentenceIndex ?? this.sentenceIndex,
      body: body ?? this.body,
      startMs: startMs ?? this.startMs,
      endMs: endMs ?? this.endMs,
      wer: wer ?? this.wer,
      difficulty: difficulty ?? this.difficulty,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (episodeId.present) {
      map['episode_id'] = Variable<String>(episodeId.value);
    }
    if (sentenceIndex.present) {
      map['index'] = Variable<int>(sentenceIndex.value);
    }
    if (body.present) {
      map['text'] = Variable<String>(body.value);
    }
    if (startMs.present) {
      map['start_ms'] = Variable<int>(startMs.value);
    }
    if (endMs.present) {
      map['end_ms'] = Variable<int>(endMs.value);
    }
    if (wer.present) {
      map['wer'] = Variable<double>(wer.value);
    }
    if (difficulty.present) {
      map['difficulty'] = Variable<String>(difficulty.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('SentencesCompanion(')
          ..write('episodeId: $episodeId, ')
          ..write('sentenceIndex: $sentenceIndex, ')
          ..write('body: $body, ')
          ..write('startMs: $startMs, ')
          ..write('endMs: $endMs, ')
          ..write('wer: $wer, ')
          ..write('difficulty: $difficulty, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

class $NotebookEntriesTable extends NotebookEntries
    with TableInfo<$NotebookEntriesTable, NotebookEntryRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $NotebookEntriesTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _idMeta = const VerificationMeta('id');
  @override
  late final GeneratedColumn<String> id = GeneratedColumn<String>(
    'id',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _wordMeta = const VerificationMeta('word');
  @override
  late final GeneratedColumn<String> word = GeneratedColumn<String>(
    'word',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _contextMeta = const VerificationMeta(
    'context',
  );
  @override
  late final GeneratedColumn<String> context = GeneratedColumn<String>(
    'context',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _episodeIdMeta = const VerificationMeta(
    'episodeId',
  );
  @override
  late final GeneratedColumn<String> episodeId = GeneratedColumn<String>(
    'episode_id',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _sentenceIndexMeta = const VerificationMeta(
    'sentenceIndex',
  );
  @override
  late final GeneratedColumn<int> sentenceIndex = GeneratedColumn<int>(
    'sentence_index',
    aliasedName,
    true,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _meaningMeta = const VerificationMeta(
    'meaning',
  );
  @override
  late final GeneratedColumn<String> meaning = GeneratedColumn<String>(
    'meaning',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _noteMeta = const VerificationMeta('note');
  @override
  late final GeneratedColumn<String> note = GeneratedColumn<String>(
    'note',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _createdAtMeta = const VerificationMeta(
    'createdAt',
  );
  @override
  late final GeneratedColumn<DateTime> createdAt = GeneratedColumn<DateTime>(
    'created_at',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _lastModifiedMeta = const VerificationMeta(
    'lastModified',
  );
  @override
  late final GeneratedColumn<DateTime> lastModified = GeneratedColumn<DateTime>(
    'last_modified',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _syncedAtMeta = const VerificationMeta(
    'syncedAt',
  );
  @override
  late final GeneratedColumn<DateTime> syncedAt = GeneratedColumn<DateTime>(
    'synced_at',
    aliasedName,
    true,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _deletedAtMeta = const VerificationMeta(
    'deletedAt',
  );
  @override
  late final GeneratedColumn<DateTime> deletedAt = GeneratedColumn<DateTime>(
    'deleted_at',
    aliasedName,
    true,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: false,
  );
  @override
  List<GeneratedColumn> get $columns => [
    id,
    word,
    context,
    episodeId,
    sentenceIndex,
    meaning,
    note,
    createdAt,
    lastModified,
    syncedAt,
    deletedAt,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'notebook_entries';
  @override
  VerificationContext validateIntegrity(
    Insertable<NotebookEntryRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('id')) {
      context.handle(_idMeta, id.isAcceptableOrUnknown(data['id']!, _idMeta));
    } else if (isInserting) {
      context.missing(_idMeta);
    }
    if (data.containsKey('word')) {
      context.handle(
        _wordMeta,
        word.isAcceptableOrUnknown(data['word']!, _wordMeta),
      );
    } else if (isInserting) {
      context.missing(_wordMeta);
    }
    if (data.containsKey('context')) {
      context.handle(
        _contextMeta,
        this.context.isAcceptableOrUnknown(data['context']!, _contextMeta),
      );
    } else if (isInserting) {
      context.missing(_contextMeta);
    }
    if (data.containsKey('episode_id')) {
      context.handle(
        _episodeIdMeta,
        episodeId.isAcceptableOrUnknown(data['episode_id']!, _episodeIdMeta),
      );
    }
    if (data.containsKey('sentence_index')) {
      context.handle(
        _sentenceIndexMeta,
        sentenceIndex.isAcceptableOrUnknown(
          data['sentence_index']!,
          _sentenceIndexMeta,
        ),
      );
    }
    if (data.containsKey('meaning')) {
      context.handle(
        _meaningMeta,
        meaning.isAcceptableOrUnknown(data['meaning']!, _meaningMeta),
      );
    }
    if (data.containsKey('note')) {
      context.handle(
        _noteMeta,
        note.isAcceptableOrUnknown(data['note']!, _noteMeta),
      );
    }
    if (data.containsKey('created_at')) {
      context.handle(
        _createdAtMeta,
        createdAt.isAcceptableOrUnknown(data['created_at']!, _createdAtMeta),
      );
    } else if (isInserting) {
      context.missing(_createdAtMeta);
    }
    if (data.containsKey('last_modified')) {
      context.handle(
        _lastModifiedMeta,
        lastModified.isAcceptableOrUnknown(
          data['last_modified']!,
          _lastModifiedMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_lastModifiedMeta);
    }
    if (data.containsKey('synced_at')) {
      context.handle(
        _syncedAtMeta,
        syncedAt.isAcceptableOrUnknown(data['synced_at']!, _syncedAtMeta),
      );
    }
    if (data.containsKey('deleted_at')) {
      context.handle(
        _deletedAtMeta,
        deletedAt.isAcceptableOrUnknown(data['deleted_at']!, _deletedAtMeta),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {id};
  @override
  NotebookEntryRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return NotebookEntryRow(
      id: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}id'],
      )!,
      word: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}word'],
      )!,
      context: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}context'],
      )!,
      episodeId: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}episode_id'],
      ),
      sentenceIndex: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}sentence_index'],
      ),
      meaning: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}meaning'],
      ),
      note: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}note'],
      ),
      createdAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}created_at'],
      )!,
      lastModified: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}last_modified'],
      )!,
      syncedAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}synced_at'],
      ),
      deletedAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}deleted_at'],
      ),
    );
  }

  @override
  $NotebookEntriesTable createAlias(String alias) {
    return $NotebookEntriesTable(attachedDatabase, alias);
  }
}

class NotebookEntryRow extends DataClass
    implements Insertable<NotebookEntryRow> {
  final String id;
  final String word;
  final String context;
  final String? episodeId;
  final int? sentenceIndex;
  final String? meaning;
  final String? note;
  final DateTime createdAt;
  final DateTime lastModified;
  final DateTime? syncedAt;
  final DateTime? deletedAt;
  const NotebookEntryRow({
    required this.id,
    required this.word,
    required this.context,
    this.episodeId,
    this.sentenceIndex,
    this.meaning,
    this.note,
    required this.createdAt,
    required this.lastModified,
    this.syncedAt,
    this.deletedAt,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['id'] = Variable<String>(id);
    map['word'] = Variable<String>(word);
    map['context'] = Variable<String>(context);
    if (!nullToAbsent || episodeId != null) {
      map['episode_id'] = Variable<String>(episodeId);
    }
    if (!nullToAbsent || sentenceIndex != null) {
      map['sentence_index'] = Variable<int>(sentenceIndex);
    }
    if (!nullToAbsent || meaning != null) {
      map['meaning'] = Variable<String>(meaning);
    }
    if (!nullToAbsent || note != null) {
      map['note'] = Variable<String>(note);
    }
    map['created_at'] = Variable<DateTime>(createdAt);
    map['last_modified'] = Variable<DateTime>(lastModified);
    if (!nullToAbsent || syncedAt != null) {
      map['synced_at'] = Variable<DateTime>(syncedAt);
    }
    if (!nullToAbsent || deletedAt != null) {
      map['deleted_at'] = Variable<DateTime>(deletedAt);
    }
    return map;
  }

  NotebookEntriesCompanion toCompanion(bool nullToAbsent) {
    return NotebookEntriesCompanion(
      id: Value(id),
      word: Value(word),
      context: Value(context),
      episodeId: episodeId == null && nullToAbsent
          ? const Value.absent()
          : Value(episodeId),
      sentenceIndex: sentenceIndex == null && nullToAbsent
          ? const Value.absent()
          : Value(sentenceIndex),
      meaning: meaning == null && nullToAbsent
          ? const Value.absent()
          : Value(meaning),
      note: note == null && nullToAbsent ? const Value.absent() : Value(note),
      createdAt: Value(createdAt),
      lastModified: Value(lastModified),
      syncedAt: syncedAt == null && nullToAbsent
          ? const Value.absent()
          : Value(syncedAt),
      deletedAt: deletedAt == null && nullToAbsent
          ? const Value.absent()
          : Value(deletedAt),
    );
  }

  factory NotebookEntryRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return NotebookEntryRow(
      id: serializer.fromJson<String>(json['id']),
      word: serializer.fromJson<String>(json['word']),
      context: serializer.fromJson<String>(json['context']),
      episodeId: serializer.fromJson<String?>(json['episodeId']),
      sentenceIndex: serializer.fromJson<int?>(json['sentenceIndex']),
      meaning: serializer.fromJson<String?>(json['meaning']),
      note: serializer.fromJson<String?>(json['note']),
      createdAt: serializer.fromJson<DateTime>(json['createdAt']),
      lastModified: serializer.fromJson<DateTime>(json['lastModified']),
      syncedAt: serializer.fromJson<DateTime?>(json['syncedAt']),
      deletedAt: serializer.fromJson<DateTime?>(json['deletedAt']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'id': serializer.toJson<String>(id),
      'word': serializer.toJson<String>(word),
      'context': serializer.toJson<String>(context),
      'episodeId': serializer.toJson<String?>(episodeId),
      'sentenceIndex': serializer.toJson<int?>(sentenceIndex),
      'meaning': serializer.toJson<String?>(meaning),
      'note': serializer.toJson<String?>(note),
      'createdAt': serializer.toJson<DateTime>(createdAt),
      'lastModified': serializer.toJson<DateTime>(lastModified),
      'syncedAt': serializer.toJson<DateTime?>(syncedAt),
      'deletedAt': serializer.toJson<DateTime?>(deletedAt),
    };
  }

  NotebookEntryRow copyWith({
    String? id,
    String? word,
    String? context,
    Value<String?> episodeId = const Value.absent(),
    Value<int?> sentenceIndex = const Value.absent(),
    Value<String?> meaning = const Value.absent(),
    Value<String?> note = const Value.absent(),
    DateTime? createdAt,
    DateTime? lastModified,
    Value<DateTime?> syncedAt = const Value.absent(),
    Value<DateTime?> deletedAt = const Value.absent(),
  }) => NotebookEntryRow(
    id: id ?? this.id,
    word: word ?? this.word,
    context: context ?? this.context,
    episodeId: episodeId.present ? episodeId.value : this.episodeId,
    sentenceIndex: sentenceIndex.present
        ? sentenceIndex.value
        : this.sentenceIndex,
    meaning: meaning.present ? meaning.value : this.meaning,
    note: note.present ? note.value : this.note,
    createdAt: createdAt ?? this.createdAt,
    lastModified: lastModified ?? this.lastModified,
    syncedAt: syncedAt.present ? syncedAt.value : this.syncedAt,
    deletedAt: deletedAt.present ? deletedAt.value : this.deletedAt,
  );
  NotebookEntryRow copyWithCompanion(NotebookEntriesCompanion data) {
    return NotebookEntryRow(
      id: data.id.present ? data.id.value : this.id,
      word: data.word.present ? data.word.value : this.word,
      context: data.context.present ? data.context.value : this.context,
      episodeId: data.episodeId.present ? data.episodeId.value : this.episodeId,
      sentenceIndex: data.sentenceIndex.present
          ? data.sentenceIndex.value
          : this.sentenceIndex,
      meaning: data.meaning.present ? data.meaning.value : this.meaning,
      note: data.note.present ? data.note.value : this.note,
      createdAt: data.createdAt.present ? data.createdAt.value : this.createdAt,
      lastModified: data.lastModified.present
          ? data.lastModified.value
          : this.lastModified,
      syncedAt: data.syncedAt.present ? data.syncedAt.value : this.syncedAt,
      deletedAt: data.deletedAt.present ? data.deletedAt.value : this.deletedAt,
    );
  }

  @override
  String toString() {
    return (StringBuffer('NotebookEntryRow(')
          ..write('id: $id, ')
          ..write('word: $word, ')
          ..write('context: $context, ')
          ..write('episodeId: $episodeId, ')
          ..write('sentenceIndex: $sentenceIndex, ')
          ..write('meaning: $meaning, ')
          ..write('note: $note, ')
          ..write('createdAt: $createdAt, ')
          ..write('lastModified: $lastModified, ')
          ..write('syncedAt: $syncedAt, ')
          ..write('deletedAt: $deletedAt')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(
    id,
    word,
    context,
    episodeId,
    sentenceIndex,
    meaning,
    note,
    createdAt,
    lastModified,
    syncedAt,
    deletedAt,
  );
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is NotebookEntryRow &&
          other.id == this.id &&
          other.word == this.word &&
          other.context == this.context &&
          other.episodeId == this.episodeId &&
          other.sentenceIndex == this.sentenceIndex &&
          other.meaning == this.meaning &&
          other.note == this.note &&
          other.createdAt == this.createdAt &&
          other.lastModified == this.lastModified &&
          other.syncedAt == this.syncedAt &&
          other.deletedAt == this.deletedAt);
}

class NotebookEntriesCompanion extends UpdateCompanion<NotebookEntryRow> {
  final Value<String> id;
  final Value<String> word;
  final Value<String> context;
  final Value<String?> episodeId;
  final Value<int?> sentenceIndex;
  final Value<String?> meaning;
  final Value<String?> note;
  final Value<DateTime> createdAt;
  final Value<DateTime> lastModified;
  final Value<DateTime?> syncedAt;
  final Value<DateTime?> deletedAt;
  final Value<int> rowid;
  const NotebookEntriesCompanion({
    this.id = const Value.absent(),
    this.word = const Value.absent(),
    this.context = const Value.absent(),
    this.episodeId = const Value.absent(),
    this.sentenceIndex = const Value.absent(),
    this.meaning = const Value.absent(),
    this.note = const Value.absent(),
    this.createdAt = const Value.absent(),
    this.lastModified = const Value.absent(),
    this.syncedAt = const Value.absent(),
    this.deletedAt = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  NotebookEntriesCompanion.insert({
    required String id,
    required String word,
    required String context,
    this.episodeId = const Value.absent(),
    this.sentenceIndex = const Value.absent(),
    this.meaning = const Value.absent(),
    this.note = const Value.absent(),
    required DateTime createdAt,
    required DateTime lastModified,
    this.syncedAt = const Value.absent(),
    this.deletedAt = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : id = Value(id),
       word = Value(word),
       context = Value(context),
       createdAt = Value(createdAt),
       lastModified = Value(lastModified);
  static Insertable<NotebookEntryRow> custom({
    Expression<String>? id,
    Expression<String>? word,
    Expression<String>? context,
    Expression<String>? episodeId,
    Expression<int>? sentenceIndex,
    Expression<String>? meaning,
    Expression<String>? note,
    Expression<DateTime>? createdAt,
    Expression<DateTime>? lastModified,
    Expression<DateTime>? syncedAt,
    Expression<DateTime>? deletedAt,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (id != null) 'id': id,
      if (word != null) 'word': word,
      if (context != null) 'context': context,
      if (episodeId != null) 'episode_id': episodeId,
      if (sentenceIndex != null) 'sentence_index': sentenceIndex,
      if (meaning != null) 'meaning': meaning,
      if (note != null) 'note': note,
      if (createdAt != null) 'created_at': createdAt,
      if (lastModified != null) 'last_modified': lastModified,
      if (syncedAt != null) 'synced_at': syncedAt,
      if (deletedAt != null) 'deleted_at': deletedAt,
      if (rowid != null) 'rowid': rowid,
    });
  }

  NotebookEntriesCompanion copyWith({
    Value<String>? id,
    Value<String>? word,
    Value<String>? context,
    Value<String?>? episodeId,
    Value<int?>? sentenceIndex,
    Value<String?>? meaning,
    Value<String?>? note,
    Value<DateTime>? createdAt,
    Value<DateTime>? lastModified,
    Value<DateTime?>? syncedAt,
    Value<DateTime?>? deletedAt,
    Value<int>? rowid,
  }) {
    return NotebookEntriesCompanion(
      id: id ?? this.id,
      word: word ?? this.word,
      context: context ?? this.context,
      episodeId: episodeId ?? this.episodeId,
      sentenceIndex: sentenceIndex ?? this.sentenceIndex,
      meaning: meaning ?? this.meaning,
      note: note ?? this.note,
      createdAt: createdAt ?? this.createdAt,
      lastModified: lastModified ?? this.lastModified,
      syncedAt: syncedAt ?? this.syncedAt,
      deletedAt: deletedAt ?? this.deletedAt,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (id.present) {
      map['id'] = Variable<String>(id.value);
    }
    if (word.present) {
      map['word'] = Variable<String>(word.value);
    }
    if (context.present) {
      map['context'] = Variable<String>(context.value);
    }
    if (episodeId.present) {
      map['episode_id'] = Variable<String>(episodeId.value);
    }
    if (sentenceIndex.present) {
      map['sentence_index'] = Variable<int>(sentenceIndex.value);
    }
    if (meaning.present) {
      map['meaning'] = Variable<String>(meaning.value);
    }
    if (note.present) {
      map['note'] = Variable<String>(note.value);
    }
    if (createdAt.present) {
      map['created_at'] = Variable<DateTime>(createdAt.value);
    }
    if (lastModified.present) {
      map['last_modified'] = Variable<DateTime>(lastModified.value);
    }
    if (syncedAt.present) {
      map['synced_at'] = Variable<DateTime>(syncedAt.value);
    }
    if (deletedAt.present) {
      map['deleted_at'] = Variable<DateTime>(deletedAt.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('NotebookEntriesCompanion(')
          ..write('id: $id, ')
          ..write('word: $word, ')
          ..write('context: $context, ')
          ..write('episodeId: $episodeId, ')
          ..write('sentenceIndex: $sentenceIndex, ')
          ..write('meaning: $meaning, ')
          ..write('note: $note, ')
          ..write('createdAt: $createdAt, ')
          ..write('lastModified: $lastModified, ')
          ..write('syncedAt: $syncedAt, ')
          ..write('deletedAt: $deletedAt, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

abstract class _$AppDatabase extends GeneratedDatabase {
  _$AppDatabase(QueryExecutor e) : super(e);
  $AppDatabaseManager get managers => $AppDatabaseManager(this);
  late final $EpisodesTable episodes = $EpisodesTable(this);
  late final $SentencesTable sentences = $SentencesTable(this);
  late final $NotebookEntriesTable notebookEntries = $NotebookEntriesTable(
    this,
  );
  @override
  Iterable<TableInfo<Table, Object?>> get allTables =>
      allSchemaEntities.whereType<TableInfo<Table, Object?>>();
  @override
  List<DatabaseSchemaEntity> get allSchemaEntities => [
    episodes,
    sentences,
    notebookEntries,
  ];
}

typedef $$EpisodesTableCreateCompanionBuilder =
    EpisodesCompanion Function({
      required String id,
      required String title,
      required DateTime publishedDate,
      required int durationMs,
      Value<double?> avgWer,
      required DateTime lastModified,
      Value<DateTime?> downloadedAt,
      Value<String?> audioLocalPath,
      Value<int> rowid,
    });
typedef $$EpisodesTableUpdateCompanionBuilder =
    EpisodesCompanion Function({
      Value<String> id,
      Value<String> title,
      Value<DateTime> publishedDate,
      Value<int> durationMs,
      Value<double?> avgWer,
      Value<DateTime> lastModified,
      Value<DateTime?> downloadedAt,
      Value<String?> audioLocalPath,
      Value<int> rowid,
    });

final class $$EpisodesTableReferences
    extends BaseReferences<_$AppDatabase, $EpisodesTable, EpisodeRow> {
  $$EpisodesTableReferences(super.$_db, super.$_table, super.$_typedResult);

  static MultiTypedResultKey<$SentencesTable, List<SentenceRow>>
  _sentencesRefsTable(_$AppDatabase db) => MultiTypedResultKey.fromTable(
    db.sentences,
    aliasName: $_aliasNameGenerator(db.episodes.id, db.sentences.episodeId),
  );

  $$SentencesTableProcessedTableManager get sentencesRefs {
    final manager = $$SentencesTableTableManager(
      $_db,
      $_db.sentences,
    ).filter((f) => f.episodeId.id.sqlEquals($_itemColumn<String>('id')!));

    final cache = $_typedResult.readTableOrNull(_sentencesRefsTable($_db));
    return ProcessedTableManager(
      manager.$state.copyWith(prefetchedData: cache),
    );
  }
}

class $$EpisodesTableFilterComposer
    extends Composer<_$AppDatabase, $EpisodesTable> {
  $$EpisodesTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get title => $composableBuilder(
    column: $table.title,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get publishedDate => $composableBuilder(
    column: $table.publishedDate,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get durationMs => $composableBuilder(
    column: $table.durationMs,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<double> get avgWer => $composableBuilder(
    column: $table.avgWer,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get downloadedAt => $composableBuilder(
    column: $table.downloadedAt,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get audioLocalPath => $composableBuilder(
    column: $table.audioLocalPath,
    builder: (column) => ColumnFilters(column),
  );

  Expression<bool> sentencesRefs(
    Expression<bool> Function($$SentencesTableFilterComposer f) f,
  ) {
    final $$SentencesTableFilterComposer composer = $composerBuilder(
      composer: this,
      getCurrentColumn: (t) => t.id,
      referencedTable: $db.sentences,
      getReferencedColumn: (t) => t.episodeId,
      builder:
          (
            joinBuilder, {
            $addJoinBuilderToRootComposer,
            $removeJoinBuilderFromRootComposer,
          }) => $$SentencesTableFilterComposer(
            $db: $db,
            $table: $db.sentences,
            $addJoinBuilderToRootComposer: $addJoinBuilderToRootComposer,
            joinBuilder: joinBuilder,
            $removeJoinBuilderFromRootComposer:
                $removeJoinBuilderFromRootComposer,
          ),
    );
    return f(composer);
  }
}

class $$EpisodesTableOrderingComposer
    extends Composer<_$AppDatabase, $EpisodesTable> {
  $$EpisodesTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get title => $composableBuilder(
    column: $table.title,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get publishedDate => $composableBuilder(
    column: $table.publishedDate,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get durationMs => $composableBuilder(
    column: $table.durationMs,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<double> get avgWer => $composableBuilder(
    column: $table.avgWer,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get downloadedAt => $composableBuilder(
    column: $table.downloadedAt,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get audioLocalPath => $composableBuilder(
    column: $table.audioLocalPath,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$EpisodesTableAnnotationComposer
    extends Composer<_$AppDatabase, $EpisodesTable> {
  $$EpisodesTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get id =>
      $composableBuilder(column: $table.id, builder: (column) => column);

  GeneratedColumn<String> get title =>
      $composableBuilder(column: $table.title, builder: (column) => column);

  GeneratedColumn<DateTime> get publishedDate => $composableBuilder(
    column: $table.publishedDate,
    builder: (column) => column,
  );

  GeneratedColumn<int> get durationMs => $composableBuilder(
    column: $table.durationMs,
    builder: (column) => column,
  );

  GeneratedColumn<double> get avgWer =>
      $composableBuilder(column: $table.avgWer, builder: (column) => column);

  GeneratedColumn<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => column,
  );

  GeneratedColumn<DateTime> get downloadedAt => $composableBuilder(
    column: $table.downloadedAt,
    builder: (column) => column,
  );

  GeneratedColumn<String> get audioLocalPath => $composableBuilder(
    column: $table.audioLocalPath,
    builder: (column) => column,
  );

  Expression<T> sentencesRefs<T extends Object>(
    Expression<T> Function($$SentencesTableAnnotationComposer a) f,
  ) {
    final $$SentencesTableAnnotationComposer composer = $composerBuilder(
      composer: this,
      getCurrentColumn: (t) => t.id,
      referencedTable: $db.sentences,
      getReferencedColumn: (t) => t.episodeId,
      builder:
          (
            joinBuilder, {
            $addJoinBuilderToRootComposer,
            $removeJoinBuilderFromRootComposer,
          }) => $$SentencesTableAnnotationComposer(
            $db: $db,
            $table: $db.sentences,
            $addJoinBuilderToRootComposer: $addJoinBuilderToRootComposer,
            joinBuilder: joinBuilder,
            $removeJoinBuilderFromRootComposer:
                $removeJoinBuilderFromRootComposer,
          ),
    );
    return f(composer);
  }
}

class $$EpisodesTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $EpisodesTable,
          EpisodeRow,
          $$EpisodesTableFilterComposer,
          $$EpisodesTableOrderingComposer,
          $$EpisodesTableAnnotationComposer,
          $$EpisodesTableCreateCompanionBuilder,
          $$EpisodesTableUpdateCompanionBuilder,
          (EpisodeRow, $$EpisodesTableReferences),
          EpisodeRow,
          PrefetchHooks Function({bool sentencesRefs})
        > {
  $$EpisodesTableTableManager(_$AppDatabase db, $EpisodesTable table)
    : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$EpisodesTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$EpisodesTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$EpisodesTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<String> id = const Value.absent(),
                Value<String> title = const Value.absent(),
                Value<DateTime> publishedDate = const Value.absent(),
                Value<int> durationMs = const Value.absent(),
                Value<double?> avgWer = const Value.absent(),
                Value<DateTime> lastModified = const Value.absent(),
                Value<DateTime?> downloadedAt = const Value.absent(),
                Value<String?> audioLocalPath = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => EpisodesCompanion(
                id: id,
                title: title,
                publishedDate: publishedDate,
                durationMs: durationMs,
                avgWer: avgWer,
                lastModified: lastModified,
                downloadedAt: downloadedAt,
                audioLocalPath: audioLocalPath,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required String id,
                required String title,
                required DateTime publishedDate,
                required int durationMs,
                Value<double?> avgWer = const Value.absent(),
                required DateTime lastModified,
                Value<DateTime?> downloadedAt = const Value.absent(),
                Value<String?> audioLocalPath = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => EpisodesCompanion.insert(
                id: id,
                title: title,
                publishedDate: publishedDate,
                durationMs: durationMs,
                avgWer: avgWer,
                lastModified: lastModified,
                downloadedAt: downloadedAt,
                audioLocalPath: audioLocalPath,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map(
                (e) => (
                  e.readTable(table),
                  $$EpisodesTableReferences(db, table, e),
                ),
              )
              .toList(),
          prefetchHooksCallback: ({sentencesRefs = false}) {
            return PrefetchHooks(
              db: db,
              explicitlyWatchedTables: [if (sentencesRefs) db.sentences],
              addJoins: null,
              getPrefetchedDataCallback: (items) async {
                return [
                  if (sentencesRefs)
                    await $_getPrefetchedData<
                      EpisodeRow,
                      $EpisodesTable,
                      SentenceRow
                    >(
                      currentTable: table,
                      referencedTable: $$EpisodesTableReferences
                          ._sentencesRefsTable(db),
                      managerFromTypedResult: (p0) => $$EpisodesTableReferences(
                        db,
                        table,
                        p0,
                      ).sentencesRefs,
                      referencedItemsForCurrentItem: (item, referencedItems) =>
                          referencedItems.where((e) => e.episodeId == item.id),
                      typedResults: items,
                    ),
                ];
              },
            );
          },
        ),
      );
}

typedef $$EpisodesTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $EpisodesTable,
      EpisodeRow,
      $$EpisodesTableFilterComposer,
      $$EpisodesTableOrderingComposer,
      $$EpisodesTableAnnotationComposer,
      $$EpisodesTableCreateCompanionBuilder,
      $$EpisodesTableUpdateCompanionBuilder,
      (EpisodeRow, $$EpisodesTableReferences),
      EpisodeRow,
      PrefetchHooks Function({bool sentencesRefs})
    >;
typedef $$SentencesTableCreateCompanionBuilder =
    SentencesCompanion Function({
      required String episodeId,
      required int sentenceIndex,
      required String body,
      required int startMs,
      required int endMs,
      Value<double?> wer,
      Value<String?> difficulty,
      Value<int> rowid,
    });
typedef $$SentencesTableUpdateCompanionBuilder =
    SentencesCompanion Function({
      Value<String> episodeId,
      Value<int> sentenceIndex,
      Value<String> body,
      Value<int> startMs,
      Value<int> endMs,
      Value<double?> wer,
      Value<String?> difficulty,
      Value<int> rowid,
    });

final class $$SentencesTableReferences
    extends BaseReferences<_$AppDatabase, $SentencesTable, SentenceRow> {
  $$SentencesTableReferences(super.$_db, super.$_table, super.$_typedResult);

  static $EpisodesTable _episodeIdTable(_$AppDatabase db) =>
      db.episodes.createAlias(
        $_aliasNameGenerator(db.sentences.episodeId, db.episodes.id),
      );

  $$EpisodesTableProcessedTableManager get episodeId {
    final $_column = $_itemColumn<String>('episode_id')!;

    final manager = $$EpisodesTableTableManager(
      $_db,
      $_db.episodes,
    ).filter((f) => f.id.sqlEquals($_column));
    final item = $_typedResult.readTableOrNull(_episodeIdTable($_db));
    if (item == null) return manager;
    return ProcessedTableManager(
      manager.$state.copyWith(prefetchedData: [item]),
    );
  }
}

class $$SentencesTableFilterComposer
    extends Composer<_$AppDatabase, $SentencesTable> {
  $$SentencesTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get body => $composableBuilder(
    column: $table.body,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get startMs => $composableBuilder(
    column: $table.startMs,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get endMs => $composableBuilder(
    column: $table.endMs,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<double> get wer => $composableBuilder(
    column: $table.wer,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get difficulty => $composableBuilder(
    column: $table.difficulty,
    builder: (column) => ColumnFilters(column),
  );

  $$EpisodesTableFilterComposer get episodeId {
    final $$EpisodesTableFilterComposer composer = $composerBuilder(
      composer: this,
      getCurrentColumn: (t) => t.episodeId,
      referencedTable: $db.episodes,
      getReferencedColumn: (t) => t.id,
      builder:
          (
            joinBuilder, {
            $addJoinBuilderToRootComposer,
            $removeJoinBuilderFromRootComposer,
          }) => $$EpisodesTableFilterComposer(
            $db: $db,
            $table: $db.episodes,
            $addJoinBuilderToRootComposer: $addJoinBuilderToRootComposer,
            joinBuilder: joinBuilder,
            $removeJoinBuilderFromRootComposer:
                $removeJoinBuilderFromRootComposer,
          ),
    );
    return composer;
  }
}

class $$SentencesTableOrderingComposer
    extends Composer<_$AppDatabase, $SentencesTable> {
  $$SentencesTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get body => $composableBuilder(
    column: $table.body,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get startMs => $composableBuilder(
    column: $table.startMs,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get endMs => $composableBuilder(
    column: $table.endMs,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<double> get wer => $composableBuilder(
    column: $table.wer,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get difficulty => $composableBuilder(
    column: $table.difficulty,
    builder: (column) => ColumnOrderings(column),
  );

  $$EpisodesTableOrderingComposer get episodeId {
    final $$EpisodesTableOrderingComposer composer = $composerBuilder(
      composer: this,
      getCurrentColumn: (t) => t.episodeId,
      referencedTable: $db.episodes,
      getReferencedColumn: (t) => t.id,
      builder:
          (
            joinBuilder, {
            $addJoinBuilderToRootComposer,
            $removeJoinBuilderFromRootComposer,
          }) => $$EpisodesTableOrderingComposer(
            $db: $db,
            $table: $db.episodes,
            $addJoinBuilderToRootComposer: $addJoinBuilderToRootComposer,
            joinBuilder: joinBuilder,
            $removeJoinBuilderFromRootComposer:
                $removeJoinBuilderFromRootComposer,
          ),
    );
    return composer;
  }
}

class $$SentencesTableAnnotationComposer
    extends Composer<_$AppDatabase, $SentencesTable> {
  $$SentencesTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => column,
  );

  GeneratedColumn<String> get body =>
      $composableBuilder(column: $table.body, builder: (column) => column);

  GeneratedColumn<int> get startMs =>
      $composableBuilder(column: $table.startMs, builder: (column) => column);

  GeneratedColumn<int> get endMs =>
      $composableBuilder(column: $table.endMs, builder: (column) => column);

  GeneratedColumn<double> get wer =>
      $composableBuilder(column: $table.wer, builder: (column) => column);

  GeneratedColumn<String> get difficulty => $composableBuilder(
    column: $table.difficulty,
    builder: (column) => column,
  );

  $$EpisodesTableAnnotationComposer get episodeId {
    final $$EpisodesTableAnnotationComposer composer = $composerBuilder(
      composer: this,
      getCurrentColumn: (t) => t.episodeId,
      referencedTable: $db.episodes,
      getReferencedColumn: (t) => t.id,
      builder:
          (
            joinBuilder, {
            $addJoinBuilderToRootComposer,
            $removeJoinBuilderFromRootComposer,
          }) => $$EpisodesTableAnnotationComposer(
            $db: $db,
            $table: $db.episodes,
            $addJoinBuilderToRootComposer: $addJoinBuilderToRootComposer,
            joinBuilder: joinBuilder,
            $removeJoinBuilderFromRootComposer:
                $removeJoinBuilderFromRootComposer,
          ),
    );
    return composer;
  }
}

class $$SentencesTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $SentencesTable,
          SentenceRow,
          $$SentencesTableFilterComposer,
          $$SentencesTableOrderingComposer,
          $$SentencesTableAnnotationComposer,
          $$SentencesTableCreateCompanionBuilder,
          $$SentencesTableUpdateCompanionBuilder,
          (SentenceRow, $$SentencesTableReferences),
          SentenceRow,
          PrefetchHooks Function({bool episodeId})
        > {
  $$SentencesTableTableManager(_$AppDatabase db, $SentencesTable table)
    : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$SentencesTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$SentencesTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$SentencesTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<String> episodeId = const Value.absent(),
                Value<int> sentenceIndex = const Value.absent(),
                Value<String> body = const Value.absent(),
                Value<int> startMs = const Value.absent(),
                Value<int> endMs = const Value.absent(),
                Value<double?> wer = const Value.absent(),
                Value<String?> difficulty = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => SentencesCompanion(
                episodeId: episodeId,
                sentenceIndex: sentenceIndex,
                body: body,
                startMs: startMs,
                endMs: endMs,
                wer: wer,
                difficulty: difficulty,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required String episodeId,
                required int sentenceIndex,
                required String body,
                required int startMs,
                required int endMs,
                Value<double?> wer = const Value.absent(),
                Value<String?> difficulty = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => SentencesCompanion.insert(
                episodeId: episodeId,
                sentenceIndex: sentenceIndex,
                body: body,
                startMs: startMs,
                endMs: endMs,
                wer: wer,
                difficulty: difficulty,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map(
                (e) => (
                  e.readTable(table),
                  $$SentencesTableReferences(db, table, e),
                ),
              )
              .toList(),
          prefetchHooksCallback: ({episodeId = false}) {
            return PrefetchHooks(
              db: db,
              explicitlyWatchedTables: [],
              addJoins:
                  <
                    T extends TableManagerState<
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic,
                      dynamic
                    >
                  >(state) {
                    if (episodeId) {
                      state =
                          state.withJoin(
                                currentTable: table,
                                currentColumn: table.episodeId,
                                referencedTable: $$SentencesTableReferences
                                    ._episodeIdTable(db),
                                referencedColumn: $$SentencesTableReferences
                                    ._episodeIdTable(db)
                                    .id,
                              )
                              as T;
                    }

                    return state;
                  },
              getPrefetchedDataCallback: (items) async {
                return [];
              },
            );
          },
        ),
      );
}

typedef $$SentencesTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $SentencesTable,
      SentenceRow,
      $$SentencesTableFilterComposer,
      $$SentencesTableOrderingComposer,
      $$SentencesTableAnnotationComposer,
      $$SentencesTableCreateCompanionBuilder,
      $$SentencesTableUpdateCompanionBuilder,
      (SentenceRow, $$SentencesTableReferences),
      SentenceRow,
      PrefetchHooks Function({bool episodeId})
    >;
typedef $$NotebookEntriesTableCreateCompanionBuilder =
    NotebookEntriesCompanion Function({
      required String id,
      required String word,
      required String context,
      Value<String?> episodeId,
      Value<int?> sentenceIndex,
      Value<String?> meaning,
      Value<String?> note,
      required DateTime createdAt,
      required DateTime lastModified,
      Value<DateTime?> syncedAt,
      Value<DateTime?> deletedAt,
      Value<int> rowid,
    });
typedef $$NotebookEntriesTableUpdateCompanionBuilder =
    NotebookEntriesCompanion Function({
      Value<String> id,
      Value<String> word,
      Value<String> context,
      Value<String?> episodeId,
      Value<int?> sentenceIndex,
      Value<String?> meaning,
      Value<String?> note,
      Value<DateTime> createdAt,
      Value<DateTime> lastModified,
      Value<DateTime?> syncedAt,
      Value<DateTime?> deletedAt,
      Value<int> rowid,
    });

class $$NotebookEntriesTableFilterComposer
    extends Composer<_$AppDatabase, $NotebookEntriesTable> {
  $$NotebookEntriesTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get word => $composableBuilder(
    column: $table.word,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get context => $composableBuilder(
    column: $table.context,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get episodeId => $composableBuilder(
    column: $table.episodeId,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get meaning => $composableBuilder(
    column: $table.meaning,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get note => $composableBuilder(
    column: $table.note,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get createdAt => $composableBuilder(
    column: $table.createdAt,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get syncedAt => $composableBuilder(
    column: $table.syncedAt,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get deletedAt => $composableBuilder(
    column: $table.deletedAt,
    builder: (column) => ColumnFilters(column),
  );
}

class $$NotebookEntriesTableOrderingComposer
    extends Composer<_$AppDatabase, $NotebookEntriesTable> {
  $$NotebookEntriesTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get word => $composableBuilder(
    column: $table.word,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get context => $composableBuilder(
    column: $table.context,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get episodeId => $composableBuilder(
    column: $table.episodeId,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get meaning => $composableBuilder(
    column: $table.meaning,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get note => $composableBuilder(
    column: $table.note,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get createdAt => $composableBuilder(
    column: $table.createdAt,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get syncedAt => $composableBuilder(
    column: $table.syncedAt,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get deletedAt => $composableBuilder(
    column: $table.deletedAt,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$NotebookEntriesTableAnnotationComposer
    extends Composer<_$AppDatabase, $NotebookEntriesTable> {
  $$NotebookEntriesTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get id =>
      $composableBuilder(column: $table.id, builder: (column) => column);

  GeneratedColumn<String> get word =>
      $composableBuilder(column: $table.word, builder: (column) => column);

  GeneratedColumn<String> get context =>
      $composableBuilder(column: $table.context, builder: (column) => column);

  GeneratedColumn<String> get episodeId =>
      $composableBuilder(column: $table.episodeId, builder: (column) => column);

  GeneratedColumn<int> get sentenceIndex => $composableBuilder(
    column: $table.sentenceIndex,
    builder: (column) => column,
  );

  GeneratedColumn<String> get meaning =>
      $composableBuilder(column: $table.meaning, builder: (column) => column);

  GeneratedColumn<String> get note =>
      $composableBuilder(column: $table.note, builder: (column) => column);

  GeneratedColumn<DateTime> get createdAt =>
      $composableBuilder(column: $table.createdAt, builder: (column) => column);

  GeneratedColumn<DateTime> get lastModified => $composableBuilder(
    column: $table.lastModified,
    builder: (column) => column,
  );

  GeneratedColumn<DateTime> get syncedAt =>
      $composableBuilder(column: $table.syncedAt, builder: (column) => column);

  GeneratedColumn<DateTime> get deletedAt =>
      $composableBuilder(column: $table.deletedAt, builder: (column) => column);
}

class $$NotebookEntriesTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $NotebookEntriesTable,
          NotebookEntryRow,
          $$NotebookEntriesTableFilterComposer,
          $$NotebookEntriesTableOrderingComposer,
          $$NotebookEntriesTableAnnotationComposer,
          $$NotebookEntriesTableCreateCompanionBuilder,
          $$NotebookEntriesTableUpdateCompanionBuilder,
          (
            NotebookEntryRow,
            BaseReferences<
              _$AppDatabase,
              $NotebookEntriesTable,
              NotebookEntryRow
            >,
          ),
          NotebookEntryRow,
          PrefetchHooks Function()
        > {
  $$NotebookEntriesTableTableManager(
    _$AppDatabase db,
    $NotebookEntriesTable table,
  ) : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$NotebookEntriesTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$NotebookEntriesTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$NotebookEntriesTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<String> id = const Value.absent(),
                Value<String> word = const Value.absent(),
                Value<String> context = const Value.absent(),
                Value<String?> episodeId = const Value.absent(),
                Value<int?> sentenceIndex = const Value.absent(),
                Value<String?> meaning = const Value.absent(),
                Value<String?> note = const Value.absent(),
                Value<DateTime> createdAt = const Value.absent(),
                Value<DateTime> lastModified = const Value.absent(),
                Value<DateTime?> syncedAt = const Value.absent(),
                Value<DateTime?> deletedAt = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => NotebookEntriesCompanion(
                id: id,
                word: word,
                context: context,
                episodeId: episodeId,
                sentenceIndex: sentenceIndex,
                meaning: meaning,
                note: note,
                createdAt: createdAt,
                lastModified: lastModified,
                syncedAt: syncedAt,
                deletedAt: deletedAt,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required String id,
                required String word,
                required String context,
                Value<String?> episodeId = const Value.absent(),
                Value<int?> sentenceIndex = const Value.absent(),
                Value<String?> meaning = const Value.absent(),
                Value<String?> note = const Value.absent(),
                required DateTime createdAt,
                required DateTime lastModified,
                Value<DateTime?> syncedAt = const Value.absent(),
                Value<DateTime?> deletedAt = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => NotebookEntriesCompanion.insert(
                id: id,
                word: word,
                context: context,
                episodeId: episodeId,
                sentenceIndex: sentenceIndex,
                meaning: meaning,
                note: note,
                createdAt: createdAt,
                lastModified: lastModified,
                syncedAt: syncedAt,
                deletedAt: deletedAt,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$NotebookEntriesTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $NotebookEntriesTable,
      NotebookEntryRow,
      $$NotebookEntriesTableFilterComposer,
      $$NotebookEntriesTableOrderingComposer,
      $$NotebookEntriesTableAnnotationComposer,
      $$NotebookEntriesTableCreateCompanionBuilder,
      $$NotebookEntriesTableUpdateCompanionBuilder,
      (
        NotebookEntryRow,
        BaseReferences<_$AppDatabase, $NotebookEntriesTable, NotebookEntryRow>,
      ),
      NotebookEntryRow,
      PrefetchHooks Function()
    >;

class $AppDatabaseManager {
  final _$AppDatabase _db;
  $AppDatabaseManager(this._db);
  $$EpisodesTableTableManager get episodes =>
      $$EpisodesTableTableManager(_db, _db.episodes);
  $$SentencesTableTableManager get sentences =>
      $$SentencesTableTableManager(_db, _db.sentences);
  $$NotebookEntriesTableTableManager get notebookEntries =>
      $$NotebookEntriesTableTableManager(_db, _db.notebookEntries);
}
