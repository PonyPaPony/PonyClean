def render_toml(data: dict) -> str:
    lines = []

    for key, values in data.items():
        lines.append(f"{key} = [")
        for value in values:
            lines.append(f"    '{value}',")
        lines.append("]")
        lines.append("")

    return "\n".join(lines)