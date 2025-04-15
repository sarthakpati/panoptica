import os
from typing import Optional
import typer
from typing_extensions import Annotated
from importlib.metadata import version
import SimpleITK as sitk


from panoptica import Panoptica_Evaluator
from panoptica.utils import sanity_checker_with_files


def version_callback(value: bool):
    __version__ = version("panoptica")
    if value:
        typer.echo(f"panoptica CLI v{__version__}")
        raise typer.Exit()


app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]}, add_completion=False
)


@app.command()
def main(
    reference: Annotated[
        str,
        typer.Option(
            "-ref",
            "--reference",
            help="The path to the reference/ground-truth image",
        ),
    ],
    prediction: Annotated[
        str,
        typer.Option(
            "-pred",
            "--prediction",
            help="The path to the predicted image",
        ),
    ],
    config: Annotated[
        str,
        typer.Option(
            "-c",
            "--config",
            help="The path to the configuration file.",
        ),
    ],
    version: Annotated[
        Optional[bool],
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Print the version and exit.",
        ),
    ] = None,
):
    """
    Generate the panoptica evaluation report for the given reference and prediction images.
    """

    # check if files exist
    for file in [reference, prediction, config]:
        assert os.path.exists(file), f"File {file} does not exist."

    # add a basic sanity check to ensure the images are compatible
    assert sanity_checker_with_files(
        reference, prediction
    ), "The reference and prediction images do not match in dimension, size, spacing, origin, or orientation."

    ref_masks = sitk.GetArrayFromImage(sitk.ReadImage(reference))
    pred_masks = sitk.GetArrayFromImage(sitk.ReadImage(prediction))

    evaluator = Panoptica_Evaluator.load_from_config_name(config)

    print(evaluator.evaluate(pred_masks, ref_masks)["ungrouped"])


if __name__ == "__main__":
    app()
