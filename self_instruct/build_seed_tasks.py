import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        type=str,
        default=r"D:\workspace\statsmind\LLaMA-Factory\data\alpaca_data_zh_51k.json"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="data/my_seed_tasks.jsonl",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    items = [item for item in data]
    with open(args.output_file, 'w', encoding='utf-8') as fp:
        for idx, item in enumerate(items):
            if '输入' in item:
                item['input'] = item['输入']

            if '输出' in item:
                item['output'] = item['输出']

            if 'instruction' not in item or 'input' not in item or 'output' not in item:
                continue

            if not (6 <= len(item['instruction']) <= 50) or len(item['output']) == 0:
                continue

            try:
                fp.write(json.dumps({
                    'id': f'seed_task_{idx}', 'name': f'name_{idx}', 'instruction': item['instruction'],
                    'instances': [{'input': item['input'], 'output': item['output']}],
                    'is_classification': False
                }, ensure_ascii=False) + "\n")
            except Exception as ex:
                raise ex
