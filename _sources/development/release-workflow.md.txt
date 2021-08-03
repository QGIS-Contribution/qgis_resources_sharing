# Release workflow

Releasing a new version involves an upload to plugins.qgis.org, so in
order to complete the workflow you must have a user with sufficient
rights to do upload.

Follow these steps to release the plugin:

1. Update `metadata.txt`:
   - Change the `version`.
     Example: `version=0.11.1` (for point release 11.1 of
     version 0).
   - Update the `changelog` (add information about the changes in
     the new version).
     Example:
     ```
     changelog=
         0.11.0 - Check for missing repository name and URL in directory (#64)
                - Correct link to documentation
     ```
     to mention two changes, and refer issue (or PR) #64.
2. Make sure that the log level
   (set in _resource_sharing/custom_logging.py_)
   is appropriate for deployment:

   `logger.setLevel(logging.INFO)`

3. The branch to release should be `master`, so make sure you are on
   the master branch before proceeding to the next step.
   If you want to release from the `develop` branch, please make a PR
   to the `master` branch first.
4. Run `make release`.

   This will create a package from the current branch, add a GitHub
   version release tag, and publish the plugin to
   `plugin.qgis.org`.
   You will be asked for your `plugins.qgis.org` id and password.

5. Voila, the new version of the plugin should be published!
   **_Check if you can upgrade the plugin in QGIS without problems_**.
6. Make a release on Github and highlight all the new features and
   fixes of the new version.
