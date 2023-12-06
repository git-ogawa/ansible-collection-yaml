#!/usr/bin/python
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Any

import jmespath
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError

ValueType = dict[str, Union[str, int, float, bool]]


@dataclass
class YamlParser:
    path: Union[Path, str]
    update: list[ValueType]
    values: dict
    overwrite: bool = False
    changed: bool = False

    def read(self):
        try:
            with open(self.path, "r") as f:
                y = YAML()
                y.preserve_quotes = True
                y.indent(mapping=2, sequence=4, offset=2)
                self.yaml_data = y.load(f)
        except ScannerError as e:
            raise ParserError(str(e))

    def _convert(self, key: str) -> tuple[str, Optional[int]]:
        """Return key string and index if a given key list-like string.

        If key is list-like then return the splitted values.
        e.g. the input key[10] is returned as key and 10. otherwise return as is.

        Args:
            key (str): A string.

        Returns:
            tuple[str, int]: A key and index (if included).
        """
        if "[" not in key and "]" not in key:
            return key, None

        pattern = r"(.*)\[([\-0-9]*)\]"
        match = re.search(pattern, key)
        assert match
        key = match.group(1)
        if len(match.groups()) == 2:
            index = int(match.group(2))
            return key, index

    def _check(self, key: str, added: bool = False, removed: bool = False) -> None:
        split_key = key.split(".")
        v = self.yaml_data
        for i in range(len(split_key)):
            key, index = self._convert(split_key[i])
            if index is None:
                # key is expected to dict.
                if not isinstance(v, dict):
                    if added:
                        v[key] = {}
                    elif removed:
                        break
                    else:
                        depth = self._join(split_key, ".", i)
                        raise AttributeError(f"Cannot get value of {depth}")
                if not split_key[i] in v.keys():
                    if added:
                        v[key] = {}
                    elif removed:
                        break
                    else:
                        depth = self._join(split_key, ".", i + 1)
                        raise AttributeError(f"Cannot get value of {depth}")
                v = v[key]
            else:
                # key is expected to list.
                if key not in v.keys():
                    if added:
                        v[key] = [{}]
                    elif removed:
                        break
                    else:
                        depth = self._join(split_key, ".", i + 1)
                        raise AttributeError(f"Cannot get value of {depth}")
                if len(v[key]) <= index:
                    if added:
                        v[key].append({})
                    elif removed:
                        break
                    else:
                        depth = self._join(split_key, ".", i + 1)
                        raise IndexError(f"{depth} is out of index")

                v = v[key][index]

    def _join(self, l: list, delimiter: str = ".", depth: Optional[int] = None) -> str:
        """Return the original key string from the the one splitted by delimiter.

        For example, if the input is [a, b[0], c, d] and depth is not given,
        then return the original key string a.b[0].c.d. if the depth is 2, return the key up to depth 2 a.b[0].

        Args:
            l (list): A list whose elements is the key splitted by delimiter.
            delimiter (str, optional): A delimiter to split the key. Defaults to ".".
            depth (Optional[int], optional): A index to determine how depth in the original ket to get.

        Returns:
            str: The original key.
        """

        if depth is None:
            depth = len(l)
        return delimiter.join(str(x) for x in l[:depth])

    def _update(self, key_string: str, value: Any=None, removed: bool = False) -> bool:
        keys = key_string.split(".")
        temp_dict = self.yaml_data
        for key in keys[:-1]:
            if "[" in key:
                key, idx = self._convert(key)
                temp_dict = temp_dict[key][idx]
            else:
                temp_dict = temp_dict[key]

        if "[" in keys[-1]:
            key, idx = self._convert(keys[-1])
            keys[-1] = key
            try:
                if removed is True:
                    try:
                        temp_dict.pop(keys[-1][idx])
                        return True
                    except KeyError:
                        return False

                org_value = temp_dict[keys[-1]][idx]
                if org_value == value:
                    return False
                temp_dict[keys[-1]][idx] = value
                return True
            except (IndexError, KeyError):
                raise ValueError(f"Invalid index {idx} for key {key}")
        else:
            try:
                if removed is True:
                    try:
                        temp_dict.pop(keys[-1])
                        return True
                    except KeyError:
                        return False

                org_value = temp_dict[keys[-1]]
                if org_value == value:
                    return False
                temp_dict[keys[-1]] = value
                return True
            except KeyError:
                raise ValueError(f"Invalid key {keys[-1]}")

    def save(self) -> None:
        with open(self.path, "w") as f:
            y = YAML()
            y.preserve_quotes = True
            y.indent(mapping=2, sequence=4, offset=2)
            y.dump(self.yaml_data, f)

    def run(self) -> None:
        try:
            if self.update:
                for v in self.update:
                    key = str(v["key"])
                    self._check(key, v.get("added", False), v.get("removed"))

                    if self._update(str(key), v.get("value", None), removed=v.get("removed", False)) is True:
                        # Set status to changed when at least one value are updated.
                        self.changed = True


            if self.values:
                self.compare_dicts(
                    self.values, self.yaml_data, added=True, overwrite=self.overwrite
                )
        except (AttributeError, IndexError) as e:
            raise ParserError(str(e))
        except TypeError:
            raise

    def compare_dicts(
        self,
        src_dict: dict[str, Any],
        dst_dict: dict[str, Any],
        overwrite: bool,
        added: bool = True,
    ) -> None:
        for key in src_dict:
            if key not in dst_dict:
                if added:
                    dst_dict[key] = src_dict[key]
                    self.changed = True
                else:
                    raise AttributeError(f"{key} not found in target")
            elif isinstance(src_dict[key], dict) and isinstance(dst_dict[key], dict):
                # When both src and dest are dict, call method recursively.
                self.compare_dicts(
                    src_dict[key], dst_dict[key], overwrite=overwrite, added=added
                )
            elif isinstance(src_dict[key], dict) and isinstance(dst_dict[key], list):
                # When src is dict and dest is list.
                # Overwrite the dest values by src dict if overwrite is set to true, otherwise raise exception.
                if overwrite:
                    dst_dict[key] = src_dict[key]
                    self.changed = True
                else:
                    raise TypeError(
                        f"Type of {key} is dict but the one in target seem to be list"
                    )
            elif isinstance(src_dict[key], list) and isinstance(dst_dict[key], list):
                # When both src and dest are list, check the elements of src in order. .
                for i in range(len(src_dict[key])):
                    if isinstance(src_dict[key][i], list):
                        # When type of element in src-list is list ans dest is also list,
                        # check if all elements of src are contained in dest.
                        # if there are missing elements, add the element to dest.
                        if isinstance(dst_dict[key][i], list):
                            missing_keys = self._all_search(
                                src_dict[key][i], dst_dict[key]
                            )
                            if missing_keys:
                                d = {}
                                for k in missing_keys:
                                    d[k] = src_dict[key][i][k]
                                dst_dict[key].append(d)
                                self.changed = True
                        else:
                            self.compare_dicts(
                                src_dict[key][i],
                                dst_dict[key][i],
                                overwrite=overwrite,
                                added=added,
                            )

                    # If there are elements that src has and dest doesn't have, add them.'
                    if i >= len(dst_dict[key]):
                        if added:
                            dst_dict[key].append(src_dict[key][i])
                            self.changed = True
                        else:
                            raise IndexError(f"{key}[{i}] not found in target")
                    elif isinstance(src_dict[key][i], dict):
                        self.compare_dicts(
                            src_dict[key][i],
                            dst_dict[key][i],
                            overwrite=overwrite,
                            added=added,
                        )
            elif isinstance(src_dict[key], list) and isinstance(dst_dict[key], dict):
                if overwrite:
                    dst_dict[key] = src_dict[key]
                    self.changed = True
                else:
                    raise TypeError(
                        f"Type of {key} is list but the one in target seem to be dict"
                    )
            elif src_dict[key] != dst_dict[key]:
                dst_dict[key] = src_dict[key]
                self.changed = True

    def _all_search(self, dict1: dict[str, str], list1: list) -> list[str]:
        missing_keys = []
        for k, v in dict1.items():
            if not self._search(k, v, list1):
                missing_keys.append(k)
        return missing_keys

    def _search(self, key: str, value: str, list1: list) -> bool:
        ret = jmespath.search(f"[? {key} == `{value}`]", list1)
        if ret:
            return True
        return False


class ParserError(Exception):
    pass
