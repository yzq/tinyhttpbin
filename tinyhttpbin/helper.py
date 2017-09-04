ROBOT_TXT = """User-agent: *
Disallow: /deny
"""

def multidict_to_dict(md):
    if md:
        dict = md.to_dict(flat=False)
        for k, v in dict.items():
            if len(v) == 1:
                dict[k] = v[0]
        return dict
    else:
        return md
