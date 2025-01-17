# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
from biom import Table

from qiime2 import Artifact


rep_seqs_1_url = ('https://data.qiime2.org/usage-examples/'
                  'metadata/rep-seqs.qza')
rep_seqs_2_url = ('https://data.qiime2.org/usage-examples/'
                  'phylogeny/rep-seqs.qza')
taxonomy_1_url = ('https://docs.qiime2.org/jupyterbooks/cancer-microbiome-'
                  'intervention-tutorial/data/030-tutorial-downstream/020-'
                  'taxonomy/taxonomy.qza')
moving_pics_ft_url = ('https://data.qiime2.org/usage-examples/'
                      'filtering/table.qza')
moving_pics_md_url = ('https://data.qiime2.org/usage-examples/'
                      'moving-pictures/sample-metadata.tsv')
rep_seqs_dada2_url = 'https://data.qiime2.org/usage-examples/' \
                     'moving-pictures/rep-seqs-dada2.qza'
rep_seqs_deblur_url = 'https://data.qiime2.org/usage-examples/' \
                      'moving-pictures/rep-seqs-deblur.qza'


def ft1_factory():
    return Artifact.import_data(
        'FeatureTable[Frequency]',
        Table(np.array([[0, 1, 3], [1, 1, 2]]),
              ['O1', 'O2'],
              ['S1', 'S2', 'S3']))


def ft2_factory():
    return Artifact.import_data(
        'FeatureTable[Frequency]',
        Table(np.array([[0, 2, 6], [2, 2, 4]]),
              ['O1', 'O3'],
              ['S4', 'S5', 'S6']))


def ft3_factory():
    return Artifact.import_data(
        'FeatureTable[Frequency]',
        Table(np.array([[0, 4, 9], [4, 4, 8]]),
              ['O1', 'O4'],
              ['S7', 'S8', 'S9']))


def feature_table_merge_two_tables(use):
    feature_table1 = use.init_artifact('feature_table1', ft1_factory)
    feature_table2 = use.init_artifact('feature_table2', ft2_factory)

    merged_table, = use.action(
        use.UsageAction(plugin_id='feature_table',
                        action_id='merge'),
        use.UsageInputs(tables=[feature_table1, feature_table2]),
        use.UsageOutputNames(merged_table='merged_table'),
    )

    merged_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_merge_three_tables(use):
    feature_table1 = use.init_artifact('feature_table1', ft1_factory)
    feature_table2 = use.init_artifact('feature_table2', ft2_factory)
    feature_table3 = use.init_artifact('feature_table3', ft3_factory)

    merged_table, = use.action(
        use.UsageAction(plugin_id='feature_table',
                        action_id='merge'),
        use.UsageInputs(
            tables=[feature_table1, feature_table2, feature_table3],
            overlap_method='sum'
        ),
        use.UsageOutputNames(merged_table='merged_table'),
    )

    merged_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_merge_taxa(use):
    # TODO: Would probably be better to have two different artifacts here
    tax1 = use.init_artifact_from_url('tax1', taxonomy_1_url)
    tax2 = \
        use.init_artifact_from_url('tax2', taxonomy_1_url)

    merged_data, = use.action(
        use.UsageAction('feature_table', 'merge_taxa'),
        use.UsageInputs(
            data=[tax1, tax2]
        ),
        use.UsageOutputNames(
            merged_data='merged_data'
        )
    )

    merged_data.assert_output_type('FeatureData[Taxonomy]')


def feature_table_merge_seqs(use):
    dada2_seqs = use.init_artifact_from_url('seqs1', rep_seqs_dada2_url)
    deblur_seqs = use.init_artifact_from_url('seqs2', rep_seqs_deblur_url)

    merged_data, = use.action(
        use.UsageAction('feature_table', 'merge_seqs'),
        use.UsageInputs(
            data=[dada2_seqs, deblur_seqs]
        ),
        use.UsageOutputNames(
            merged_data='merged_data'
        )
    )

    merged_data.assert_output_type('FeatureData[Sequence]')


def feature_table_filter_samples_min_features(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=feature_table,
                        min_features=10),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_min_frequency(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=feature_table,
                        min_frequency=1500),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_to_subject1(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    sample_metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=feature_table, metadata=sample_metadata,
                        where='[subject]="subject-1"'),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_to_skin(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    sample_metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=feature_table, metadata=sample_metadata,
                        where='[body-site] IN ("left palm", "right palm")'),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_to_subject1_gut(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    sample_metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(table=feature_table, metadata=sample_metadata,
                        where=r'[subject]="subject-1" AND [body-site]="gut"'),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_to_gut_or_abx(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    sample_metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(
            table=feature_table, metadata=sample_metadata,
            where=r'[body-site]="gut" OR [reported-antibiotic-usage]="Yes"'),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_samples_to_subject1_not_gut(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    sample_metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table', action_id='filter_samples'),
        use.UsageInputs(
            table=feature_table, metadata=sample_metadata,
            where=r'[subject]="subject-1" AND NOT [body-site]="gut"'),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_features_min_samples(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table',
                        action_id='filter_features'),
        use.UsageInputs(table=feature_table,
                        min_samples=2),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_filter_features_conditionally(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )

    use.comment("Retain only features with at least 1%% abundance in at "
                "least 34%% of samples.")

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table',
                        action_id='filter_features_conditionally'),
        use.UsageInputs(table=feature_table,
                        abundance=0.01,
                        prevalence=0.34),
        use.UsageOutputNames(filtered_table='filtered_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_group_samples(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )
    metadata = use.init_metadata_from_url(
        'sample_metadata', moving_pics_md_url,
    )
    metadata_col = use.get_metadata_column('body-site', 'body-site', metadata)

    use.comment("Combine samples from the same body-site into single sample. "
                "Feature frequencies will be the median across the samples "
                "being combined, rounded up to the nearest whole number.")

    filtered_table, = use.action(
        use.UsageAction(plugin_id='feature_table',
                        action_id='group'),
        use.UsageInputs(table=feature_table,
                        metadata=metadata_col,
                        mode='median-ceiling',
                        axis='sample'),
        use.UsageOutputNames(grouped_table='body_site_table')
    )

    filtered_table.assert_output_type('FeatureTable[Frequency]')


def feature_table_summarize(use):
    feature_table = use.init_artifact_from_url(
        'feature_table', moving_pics_ft_url
    )

    viz, = use.action(
        use.UsageAction('feature_table', 'summarize'),
        use.UsageInputs(table=feature_table),
        use.UsageOutputNames(visualization='table')
    )

    viz.assert_output_type('Visualization')


def feature_table_tabulate_seqs(use):
    rep_seqs = use.init_artifact_from_url(
        'rep_seqs', rep_seqs_1_url
    )

    viz, = use.action(
        use.UsageAction('feature_table', 'tabulate_seqs'),
        use.UsageInputs(data=rep_seqs),
        use.UsageOutputNames(visualization='rep-seqs')
    )

    viz.assert_output_type('Visualization')
