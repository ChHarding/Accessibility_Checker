import pandas as pd

def build_contrast_df(results):
    columns_contrast = ['snippet', 'label', 'ratio', 'AA', 'AAA']
    if not results:
        return pd.DataFrame(columns=columns_contrast)

    df_contrast = pd.DataFrame(results)

    # Create labels
    def make_label(row):
        label = row.get('tag', '')
        if row.get('id'):
            label += '#' + row['id']
        elif row.get('classes'):
            label += '.' + row['classes']
        return label

    df_contrast['label'] = df_contrast.apply(make_label, axis=1)

    # return only desired columns
    return df_contrast[['snippet', 'label', 'ratio', 'AA', 'AAA']]

def format_contrast_results(results):
    df = build_contrast_df(results)
    if df.empty:
        print("No contrast issues!")
        return
    print(df.to_markdown(index=False))


def get_contrast_json(results): # AI helped
    df = build_contrast_df(results)
    grouped = {}
    for snippet, group in df.groupby('snippet'):
        grouped[snippet] = group[['label', 'ratio', 'AA', 'AAA']].to_dict(orient='records')
    return grouped

# Typography formatters ----------

def build_typography_df(results):
    cols = ['snippet', 'label', 'size_px', 'WCAG']
    if not results:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(results)
    def make_label(row):
        label = row.get('tag', '')
        if row.get('id'):
            label += '#' + row['id']
        elif row.get('classes'):
            label += '.' + row['classes']
        return label
    df['label'] = df.apply(make_label, axis=1)
    return df[['snippet', 'label', 'size_px', 'WCAG']]

def format_typography_results(results):
    df = build_typography_df(results)
    if df.empty:
        print("No typography issues!")
        return
    print(df.to_markdown(index=False))

def get_typography_json(results):
    df = build_typography_df(results)
    grouped = {}
    for snippet, group in df.groupby('snippet'):
        grouped[snippet] = group[['label', 'size_px', 'WCAG']].to_dict(orient='records')
    return grouped

# Alt-Text formatters ----------

def build_alt_text_df(results):
    cols = ['src_label', 'alt', 'status']
    if not results:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(results)
    # Derive filename from src URL/path AI helped
    df['src_label'] = df['src'].apply(lambda s: s.split('/')[-1])
    return df[['src_label', 'alt', 'status']]

def format_alt_text_results(results):
    df = build_alt_text_df(results)
    if df.empty:
        print("No alt-text results!")
        return
    print(df.to_markdown(index=False))

def get_alt_text_json(results):
    df = build_alt_text_df(results)
    return df.to_dict(orient='records')

# Heading structure formatters ----------

def build_heading_df(results):
    columns_heading = ['warning']
    if not results:
        return pd.DataFrame(columns=columns_heading)
    return pd.DataFrame({ 'warning': results })

def format_heading_results(results):
    df = build_heading_df(results)
    if df.empty:
        print("All headings are in good order!")
        return
    print(df.to_markdown(index=False))

def get_heading_json(results):
    df = build_heading_df(results)
    return df.to_dict(orient='records')

# Buttor Formatters ---------------
def build_button_df(failures):
    columns_buttons = ['label', 'status']
    if not failures:
        return pd.DataFrame(columns=columns_buttons)
    return pd.DataFrame(failures)[columns_buttons]

def format_button_results(failures):
    df = build_button_df(failures)

    if df.empty:
        print("All buttons have text or aria-labels")
    else:
        print("Missing link/button labels:")
        print(df.to_markdown(index=False))

def get_button_json(failures):
    return build_button_df(failures).to_dict(orient='records')
