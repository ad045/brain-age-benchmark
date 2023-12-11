# first line: 65
@failsafe_run(
    get_input_fnames=get_input_fnames_data_quality,
)
def assess_data_quality(
    *,
    cfg: SimpleNamespace,
    exec_params: SimpleNamespace,
    subject: str,
    session: Optional[str],
    run: Optional[str],
    task: Optional[str],
    in_files: dict,
) -> dict:
    """Assess data quality and find and mark bad channels."""
    import matplotlib.pyplot as plt

    out_files = dict()
    key = f"raw_task-{task}_run-{run}"
    bids_path_in = in_files.pop(key)
    if _do_mf_autobad(cfg=cfg):
        if key == "raw_task-noise_run-None":
            bids_path_ref_in = in_files.pop("raw_ref_run")
        else:
            bids_path_ref_in = None
        auto_scores = _find_bads_maxwell(
            cfg=cfg,
            exec_params=exec_params,
            bids_path_in=bids_path_in,
            bids_path_ref_in=bids_path_ref_in,
            subject=subject,
            session=session,
            run=run,
            task=task,
            out_files=out_files,
        )
    else:
        auto_scores = None
    del key

    # Report
    with _open_report(
        cfg=cfg,
        exec_params=exec_params,
        subject=subject,
        session=session,
        run=run,
        task=task,
    ) as report:
        # Original data
        kind = "original" if not cfg.proc else cfg.proc
        msg = f"Adding {kind} raw data to report"
        logger.info(**gen_log_kwargs(message=msg))
        _add_raw(
            cfg=cfg,
            report=report,
            bids_path_in=bids_path_in,
            title=f"Raw ({kind})",
            tags=("data-quality",),
        )
        if cfg.find_noisy_channels_meg:
            assert auto_scores is not None
            msg = "Adding noisy channel detection to report"
            logger.info(**gen_log_kwargs(message=msg))
            figs = plot_auto_scores(auto_scores, ch_types=cfg.ch_types)
            captions = [f"Run {run}"] * len(figs)
            tags = ("raw", "data-quality", f"run-{run}")
            report.add_figure(
                fig=figs,
                caption=captions,
                section="Data quality",
                title=f"Bad channel detection: {run}",
                tags=tags,
                replace=True,
            )
            for fig in figs:
                plt.close(fig)

    assert len(in_files) == 0, in_files.keys()
    return _prep_out_files(exec_params=exec_params, out_files=out_files)
