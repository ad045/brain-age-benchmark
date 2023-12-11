# first line: 57
@failsafe_run(
    get_input_fnames=get_input_fnames_find_empty_room,
)
def find_empty_room(
    *,
    cfg: SimpleNamespace,
    exec_params: SimpleNamespace,
    subject: str,
    session: Optional[str],
    run: Optional[str],
    in_files: Dict[str, BIDSPath],
) -> Dict[str, BIDSPath]:
    raw_path = in_files.pop(f"raw_run-{run}")
    in_files.pop("sidecar", None)
    try:
        fname = raw_path.find_empty_room(use_sidecar_only=True)
    except (FileNotFoundError, AssertionError, ValueError):
        fname = ""
    if fname is None:
        # sidecar is very fast and checking all can be slow (seconds), so only
        # log when actually looking through files
        ending = "empty-room files"
        if len(in_files):  # MNE-BIDS < 0.12 missing get_empty_room_candidates
            ending = f"{len(in_files)} empty-room file{_pl(in_files)}"
        msg = f"Nearest-date matching {ending}"
        logger.info(**gen_log_kwargs(message=msg))
        try:
            fname = raw_path.find_empty_room()
        except (
            ValueError,  # non-MEG data
            AssertionError,  # MNE-BIDS check assert exists()
            FileNotFoundError,
        ):  # MNE-BIDS PR-1080 exists()
            fname = None
        in_files.clear()  # MNE-BIDS find_empty_room should have looked at all
    elif fname == "":
        fname = None  # not downloaded, or EEG data
    elif not fname.fpath.exists():
        fname = None  # path found by sidecar but does not exist
    out_files = dict()
    out_files["empty_room_match"] = _empty_room_match_path(raw_path, cfg)
    _write_json(out_files["empty_room_match"], dict(fname=fname))
    return _prep_out_files(exec_params=exec_params, out_files=out_files)
