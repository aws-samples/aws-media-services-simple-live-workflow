# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Third-party patches are essential for growing and enhancing AWS Media Services Simple Live Workflow. We want to keep it as easy as possible to contribute changes that
get things working in your environment. There are a few guidelines that we
need contributors to follow so that we can have a chance of keeping on
top of things.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## AWS Media Services Simple Live Workflow Changes

New functionality is typically directed toward **extra-modules** to provide a slimmer
core workshop, reducing its surface area, and to allow greater freedom for
module maintainers to ship releases at their own cadence. 

Generally, new types, non-backward compatible and OS-specific changes should be added as backward compatible enhancements. Exceptions would be things like new cross-OS features
and updates to existing core workshop.

If you are unsure of whether your contribution should be implemented as a
extension or part of AWS Media Services Simple Live Workflow, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Revert Policy

By running tests in advance and by engaging with peer review for prospective
changes, your contributions have a high probability of becoming long lived
parts of the the project. After being merged, the code will run through a
series of testing pipelines on a large number of operating system
environments. These pipelines can reveal incompatibilities that are difficult
to detect in advance.

If the code change results in a test failure, we will make our best effort to
correct the error. If a fix cannot be determined and committed within 24 hours
of its discovery, the commit(s) responsible _may_ be reverted, at the
discretion of the committer and AWS Media Services Simple Live Workflow maintainers. This action would be taken
to help maintain passing states in our testing pipelines.

The original contributor will be notified of the revert in the Issue
associated with the change. A reference to the test(s) and operating system(s)
that failed as a result of the code change will also be added to the Issue. This test(s) should be used to check future submissions of the code to
ensure the issue has been resolved.




