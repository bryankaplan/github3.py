# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Gist."""
from .helper import IntegrationHelper

import github3


class TestGist(IntegrationHelper):

    """Gist integration tests."""

    def test_comments(self):
        """Show that a user can iterate over the comments on a gist."""
        cassette_name = self.cassette_name('comments')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist(3342247)
            assert gist is not None
            for comment in gist.comments():
                assert isinstance(comment, github3.gists.comment.GistComment)

    def test_create_comment(self):
        """Show that a user can comment on a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('create_comment')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist('f396190a0d0047be791b')
            assert gist is not None
            c = gist.create_comment("""```ruby
            mac.split('').map.with_index do |v, i|
              positions.include?(i) ? ':' + v : v
            end
            ```""")
            assert isinstance(c, github3.gists.comment.GistComment)

    def test_commits(self):
        """Show that a user can iterate over the commits in a gist."""
        cassette_name = self.cassette_name('commits')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            gist = self.gh.gist(1834570)
            assert gist is not None
            for commit in gist.commits():
                assert isinstance(commit, github3.gists.history.GistHistory)

    def test_delete(self):
        """Show that a user can delete a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.create_gist(
                'Title', {
                    'filename.py': {
                        'content': '# -*- coding: utf-8 -*-'
                    }
                }
            )
            assert isinstance(gist, github3.gists.Gist)
            assert gist.delete() is True

    def test_edit(self):
        """Show that a user can edit the contents of a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist(6647085)
            assert gist is not None
            assert gist.edit('Updated description', files={
                'filename.py': {
                    'content': '# New content',
                },
                'new_file.py': {
                    'content': '# New file content',
                },
            }) is True

    def test_fork(self):
        """Show that a user can fork another user's gist."""
        self.basic_login()
        cassette_name = self.cassette_name('fork')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist('8de9b9b0ae2e45383d85')
            assert gist is not None
            forked = gist.fork()
            assert isinstance(forked, github3.gists.Gist)
            assert str(forked.owner) == 'sigmavirus24'

    def test_forks(self):
        """Show that a user can iterate over the forks of a gist."""
        cassette_name = self.cassette_name('forks')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            gist = self.gh.gist(1834570)
            assert gist is not None
            for commit in gist.forks():
                assert isinstance(commit, github3.gists.gist.Gist)

    def test_is_starred(self):
        """Show that a user can check if they've starred a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('is_starred')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist(1834570)
            assert gist is not None
            assert gist.is_starred() is True

    def test_star(self):
        """Show that a user can star a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('star')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist('8de9b9b0ae2e45383d85')
            assert gist is not None
            assert gist.star() is True

    def test_unstar(self):
        """Show that a user can unstar a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('unstar')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist('8de9b9b0ae2e45383d85')
            assert gist is not None
            assert gist.unstar() is True
